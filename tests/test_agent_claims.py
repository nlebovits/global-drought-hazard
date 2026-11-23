#!/usr/bin/env python3
"""Regenerate every stated number in the AGENTS.md files from the live data.

A stated number sits between claim markers. An optional format after the id
spells the value as a word (`words`, `Words`) or wraps it in backticks (`code`):

    <!-- claim:valid-pct-1.0 -->25.99<!-- /claim -->
    <!-- claim:band-count Words -->One<!-- /claim -->

In Markdown, a line that starts with "<!--" opens an HTML block. So a marker
never starts a line of running text: wrap the line before it, or end the line
right after the opening marker, and the script keeps that line break.

A `claim-sources` comment next to the claim holds the command that prints the
value, and the tool versions it last ran with:

    <!-- claim-sources
    valid-pct-1.0: duckdb -noheader -list -c "SELECT ..."
    tools: GDAL 3.12.4, DuckDB v2.0.0
    -->

A marker pair can wrap a ```sql or ```bash fence instead. The fence code is the
command. The comment lines at the end of the fence are its output, under a
line that names the tool versions. SQL runs as `duckdb -csv -noheader -c`, and
the script aligns the columns. Bash runs as `bash -eo pipefail -c`, and the
script strips each output line.

Every command runs against the published objects. The script then rewrites
the text between the markers and every tools line. Without --write it prints
the diff against the committed files and exits 1 if there is one. With
--write it saves the regenerated files.

Needs: duckdb (CLI), GDAL command-line tools, curl, and python3 on PATH. Use
the GDAL and DuckDB versions pinned in .github/workflows/live-claims.yml, or
the tools lines change.

Run: python3 tests/test_agent_claims.py [--write]
"""
from __future__ import annotations

import csv
import difflib
import io
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CLAIM = re.compile(
    r"<!-- claim:(?P<id>[A-Za-z0-9._-]+)(?: (?P<fmt>words|Words|code))? -->"
    r"(?P<value>.*?)<!-- /claim -->",
    re.S,
)
SOURCES = re.compile(
    r"^(?P<indent>[ \t]*)<!-- claim-sources\n(?P<body>.*?)\n[ \t]*-->[ \t]*$",
    re.M | re.S,
)
FENCE = re.compile(r"^```(?P<lang>sql|bash)\n(?P<body>.*?)^```[ \t]*$", re.M | re.S)
NUMERIC = re.compile(r"-?\d+(?:\.\d+)?")

ONES = ("zero one two three four five six seven eight nine ten eleven twelve "
        "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
ATTEMPTS = 3


class ClaimError(Exception):
    pass


def words(n: int) -> str:
    if 0 <= n < 20:
        return ONES[n]
    if 20 <= n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + ("-" + ONES[ones] if ones else "")
    raise ClaimError(f"no word form for {n}")


def tool_versions() -> str:
    gdal = subprocess.run(["gdalinfo", "--version"], capture_output=True, text=True, check=True)
    duck = subprocess.run(["duckdb", "--version"], capture_output=True, text=True, check=True)
    g = re.match(r"GDAL (\d[\d.]*)", gdal.stdout)
    d = re.match(r"(v\d[\d.]*)", duck.stdout)
    if not g or not d:
        raise ClaimError(f"cannot read tool versions: {gdal.stdout!r} {duck.stdout!r}")
    return f"GDAL {g[1]}, DuckDB {d[1]}"


_cache: dict[tuple[str, str], str] = {}


def run(lang: str, code: str) -> str:
    """Run a command in an empty directory and return its stdout. Retry network flakes."""
    key = (lang, code)
    if key in _cache:
        return _cache[key]
    if lang == "sql":
        argv = ["duckdb", "-csv", "-noheader", "-c", code]
    else:
        argv = ["bash", "-eo", "pipefail", "-c", code]
    for attempt in range(1, ATTEMPTS + 1):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(argv, capture_output=True, text=True, cwd=tmp, timeout=900)
        if result.returncode == 0:
            _cache[key] = result.stdout
            return result.stdout
        if attempt < ATTEMPTS:
            time.sleep(10 * attempt)
    raise ClaimError(f"exit {result.returncode} after {ATTEMPTS} attempts\n"
                     f"command: {code}\n{result.stderr.strip()[-800:]}")


def value(command: str, fmt: str | None) -> str:
    out = run("bash", command).strip()
    if not out or "\n" in out:
        raise ClaimError(f"a claim command must print one line, got {out!r}\ncommand: {command}")
    if fmt in ("words", "Words"):
        if not out.isdigit():
            raise ClaimError(f"format {fmt} needs an integer, got {out!r}")
        out = words(int(out))
        return out.capitalize() if fmt == "Words" else out
    if fmt == "code":
        return f"`{out}`"
    return out


def align(rows: list[list[str]]) -> list[str]:
    """Align CSV rows into columns: numbers right, text left, two spaces apart."""
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    lines = []
    for r in rows:
        cells = [c.rjust(w) if NUMERIC.fullmatch(c) else c.ljust(w) for c, w in zip(r, widths)]
        lines.append("  ".join(cells).rstrip())
    return lines


def regenerate_fence(lang: str, body: str, tools: str) -> str:
    """Rebuild a fence: keep its code, replace the trailing comment lines with fresh output."""
    mark = "--" if lang == "sql" else "#"
    lines = body.splitlines()
    while lines and lines[-1].strip().startswith(mark) and not lines[-1].startswith("#!"):
        lines.pop()
    code = "\n".join(lines)
    out = run(lang, code)
    if lang == "sql":
        rows = [r for r in csv.reader(io.StringIO(out)) if r]
        result = align(rows) if rows else []
    else:
        result = [line.strip() for line in out.splitlines() if line.strip()]
    if not result:
        raise ClaimError(f"no output from the fence\n{code}")
    comments = [f"{mark} Output ({tools}):"] + [f"{mark} {line}" for line in result]
    return "\n".join(lines + comments) + "\n"


def parse_sources(text: str, where: str) -> dict[str, str]:
    sources: dict[str, str] = {}
    for block in SOURCES.finditer(text):
        for line in block["body"].splitlines():
            line = line.strip()
            if not line or line.startswith("tools:"):
                continue
            claim_id, sep, command = line.partition(": ")
            if not sep:
                raise ClaimError(f"{where}: a claim-sources line needs 'id: command': {line!r}")
            if "-->" in command:
                raise ClaimError(f"{where}: a command cannot contain '-->': {claim_id}")
            if sources.get(claim_id, command) != command:
                raise ClaimError(f"{where}: two different commands for claim {claim_id}")
            sources[claim_id] = command
    return sources


def regenerate(text: str, where: str, tools: str) -> str:
    sources = parse_sources(text, where)
    used: set[str] = set()
    fence_spans: list[tuple[int, int]] = []

    def claim(m: re.Match) -> str:
        inner = m["value"]
        fence = FENCE.search(inner)
        if fence:
            fence_spans.append(m.span())
            new = regenerate_fence(fence["lang"], fence["body"], tools)
            inner = inner[: fence.start("body")] + new + inner[fence.end("body"):]
        else:
            if m["id"] not in sources:
                raise ClaimError(f"{where}: claim {m['id']} has no claim-sources entry")
            used.add(m["id"])
            # Keep a line break after the opening marker: a line that starts
            # with "<!--" would start an HTML block, not continue the text.
            lead, _, trail = re.fullmatch(r"(\s*)(.*?)(\s*)", inner, re.S).groups()
            inner = lead + value(sources[m["id"]], m["fmt"]) + trail
        fmt = f" {m['fmt']}" if m["fmt"] else ""
        return f"<!-- claim:{m['id']}{fmt} -->{inner}<!-- /claim -->"

    new = CLAIM.sub(claim, text)

    for fence in FENCE.finditer(text):
        if not any(a <= fence.start() < b for a, b in fence_spans):
            line = text[: fence.start()].count("\n") + 1
            raise ClaimError(f"{where}:{line}: a {fence['lang']} fence outside claim markers")
    unused = sorted(set(sources) - used)
    if unused:
        raise ClaimError(f"{where}: claim-sources entries with no claim: {unused}")

    def tools_line(m: re.Match) -> str:
        indent = m["indent"]
        body = re.sub(r"^([ \t]*)tools:.*$", rf"\g<1>tools: {tools}", m["body"], flags=re.M)
        if not re.search(r"^[ \t]*tools:", body, re.M):
            body += f"\n{indent}tools: {tools}"
        return f"{indent}<!-- claim-sources\n{body}\n{indent}-->"

    return SOURCES.sub(tools_line, new)


def main() -> int:
    write = "--write" in sys.argv[1:]
    tools = tool_versions()
    print(f"tools: {tools}")
    guides = sorted(p for p in ROOT.rglob("AGENTS.md") if ".git" not in p.relative_to(ROOT).parts)
    failures, changed = [], []
    for guide in guides:
        rel = guide.relative_to(ROOT).as_posix()
        old = guide.read_text()
        try:
            new = regenerate(old, rel, tools)
        except ClaimError as e:
            msg = str(e)
            failures.append(msg if msg.startswith(rel) else f"{rel}: {msg}")
            continue
        claims = len(CLAIM.findall(old))
        if new == old:
            print(f"ok   {rel} ({claims} claims)")
            continue
        changed.append(rel)
        if write:
            guide.write_text(new)
            print(f"wrote {rel} ({claims} claims)")
        else:
            sys.stdout.writelines(difflib.unified_diff(
                old.splitlines(keepends=True), new.splitlines(keepends=True),
                fromfile=f"a/{rel}", tofile=f"b/{rel}"))
    for f in failures:
        print(f"FAIL {f}")
    if changed and not write:
        print(f"\nFAIL regenerated text differs from the committed text in {changed}.\n"
              "Run python3 tests/test_agent_claims.py --write with the pinned tools and commit.")
    return 1 if failures or (changed and not write) else 0


if __name__ == "__main__":
    sys.exit(main())
