"""Build an index of every case: topic, domain, dimension, tier, A's hedge, author.

Reads the case files without running them (it parses the CASE literal), so it is
safe to point at teammates' branches.

Usage (from the repo root):
    uv run python tools/case_index.py                 # cases on this branch
    uv run python tools/case_index.py --all-branches  # every origin branch too

The index is printed, not committed: it reads everyone's branches, so a saved copy
goes stale with every push. Use --out FILE only for a local copy.

Run `git fetch origin` first when using --all-branches.
"""

import argparse
import ast
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

CASE_FILE = re.compile(r"^cases/m\d+\.py$")
HEDGE = re.compile(r"""hedge[^'"]{0,20}['"]([^'"]{3,40})['"]""", re.IGNORECASE)
FILLER_WORDS = {"is", "are", "it", "that", "to", "be", "have", "been", "has"}
APPROX = re.compile(r"\b(about|around|roughly|approximately|some|nearly|almost|"
                    r"close to|just over|just under)\b", re.IGNORECASE)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True,
                            encoding="utf-8")
    return result.stdout if result.returncode == 0 else ""


def parse_case(source: str) -> dict | None:
    """Return the CASE dict and docstring from a case file, without executing it."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "CASE"):
            try:
                case = ast.literal_eval(node.value)
            except ValueError:
                return None
            case["_doc"] = ast.get_docstring(tree) or ""
            return case
    return None


def topic(case: dict) -> str:
    first = case["_doc"].splitlines()[0] if case["_doc"] else ""
    first = re.sub(r"^M\d+:\s*", "", first).rstrip(".")
    return first or case.get("question", "")


def hedge(case: dict) -> str:
    """A's T1 cue: the named hedge, else an approximation word in A's content."""
    if case.get("difficulty_tier") == "T2":
        return "(none, T2)"
    for text in (case.get("design_notes", ""), case["_doc"]):
        match = HEDGE.search(text)
        if match:
            return match.group(1).strip()
    content = case.get("sources", {}).get("A", {}).get("content", "")
    match = APPROX.search(content)
    if match:
        return f"approximation: '{match.group(1).lower()}'"
    return "?"


def hedge_key(text: str) -> str:
    """Reduce a hedge to its main word, so 'is believed to have' == 'is believed to'."""
    words = [w for w in re.findall(r"[a-z]+", text.lower()) if w not in FILLER_WORDS]
    return words[0] if words else text.lower()


def first_author(path: str, ref: str | None = None) -> str:
    args = ["log", "--diff-filter=A", "--format=%an"]
    if ref:
        args.append(ref)
    out = git(*args, "--", path).strip().splitlines()
    return out[-1] if out else "?"


def local_cases() -> dict:
    found = {}
    for path in sorted(Path("cases").glob("m*.py")):
        rel = path.as_posix()
        case = parse_case(path.read_text(encoding="utf-8"))
        if case:
            found[case["case_id"]] = (case, first_author(rel), ["(this branch)"])
    return found


def branch_cases(found: dict) -> None:
    refs = [r for r in git("for-each-ref", "--format=%(refname:short)",
                           "refs/remotes/origin").split() if not r.endswith("/HEAD")]
    for ref in refs:
        for rel in git("ls-tree", "-r", "--name-only", ref, "--", "cases").split():
            if not CASE_FILE.match(rel):
                continue
            case = parse_case(git("show", f"{ref}:{rel}"))
            if not case:
                continue
            cid = case["case_id"]
            if cid not in found:
                found[cid] = (case, first_author(rel, ref), [])
            found[cid][2].append(ref.removeprefix("origin/"))


def table(found: dict) -> str:
    rows = ["| Case | Topic | Domain | Dimension | Tier | A's cue | Author "
            "| Branches |",
            "|---|---|---|---|---|---|---|---|"]
    for cid in sorted(found, key=lambda c: int(re.sub(r"\D", "", c) or 0)):
        case, author, branches = found[cid]
        others = sorted(set(branches) - {"(this branch)"})
        if "main" in others:
            shown = "main"
        elif others:
            shown = ", ".join(others[:3]) + (f" (+{len(others) - 3})"
                                             if len(others) > 3 else "")
        else:
            shown = "(this branch only)"
        rows.append(f"| {cid} | {topic(case)} | {case.get('domain', '')} | "
                    f"{case.get('quality_dimension', '')} | "
                    f"{case.get('difficulty_tier', '')} | {hedge(case)} | {author} | "
                    f"{shown} |")
    return "\n".join(rows)


MAX_PER_HEDGE = 3  # R16: at most three T1 cases share a hedge


def hedges_in_use(found: dict) -> str:
    """Every hedge in use, by main word, with its cases and how many slots are left."""
    groups = defaultdict(list)
    for cid, (case, _, _) in found.items():
        h = hedge(case)
        if h not in ("(none, T2)", "?") and not h.startswith("approximation"):
            groups[hedge_key(h)].append(f"{cid} ('{h}')")
    lines = []
    for key, ids in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        left = MAX_PER_HEDGE - len(ids)
        status = "full" if left == 0 else ("over limit" if left < 0 else
                                          f"{left} left")
        ids = sorted(ids, key=lambda s: int(re.sub(r"\D", "", s.split()[0]) or 0))
        lines.append(f"- **{key}** ({len(ids)}, {status}): {', '.join(ids)}")
    return "\n".join(lines) if lines else "None."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--all-branches", action="store_true",
                        help="also read cases from every origin/* branch")
    parser.add_argument("--out", help="write the index to this Markdown file")
    args = parser.parse_args()

    found = local_cases()
    if args.all_branches:
        branch_cases(found)
    report = ("# Case index\n\nGenerated by `tools/case_index.py`; do not edit by "
              "hand.\n\n" + table(found) + "\n\n## Hedges in use (at most "
              f"{MAX_PER_HEDGE} cases each)\n\n" + hedges_in_use(found) + "\n")
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Wrote {args.out} ({len(found)} cases)")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(report)


if __name__ == "__main__":
    main()