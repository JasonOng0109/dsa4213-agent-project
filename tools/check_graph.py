"""
Checks knowledge-graph.html against the repository. No API calls. The test suite runs
it too (tests/test_graph.py), so a quote that stops matching its file fails the suite.

    uv run python tools/check_graph.py

Errors (exit code 1):
- a node without a summary, or without at least one evidence quote;
- a quote that no longer appears in its file -- the source changed, so the node
  may have drifted; re-read the file and update or supersede the node;
- an `absent` string that now appears, or a `missing` file that now exists --
  the drift item that cites it may be resolved;
- a link, [[ref]] or changelog id that names no node; a cycle in "needs".
Warnings: a quote that moved to another line or page than its `loc` says.
"""

import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "knowledge-graph.html"
TYPES = {"question", "concept", "claim", "design", "decision", "finding",
         "literature", "process", "risk", "issue"}
STATUSES = {"current", "superseded", "open", "drift"}
RELS = {"needs", "tests", "supports", "challenges", "because", "motivates",
        "replaces", "part-of", "involves", "limits", "related"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'),
                 ("–", "-"), ("—", "-"), ("−", "-"), ("\\$", "$")):
        s = s.replace(a, b)
    s = re.sub(r"^\s*>\s?", "", s)      # markdown blockquote marker
    s = re.sub(r"[*`]", "", s)          # markdown emphasis and code marks
    return re.sub(r"\s+", " ", s).strip()


_units = {}


def units_of(path: Path) -> list[str] | None:
    """Normalized text units: lines for text files, pages for PDFs."""
    if path not in _units:
        if path.suffix == ".pdf":
            if not shutil.which("pdftotext"):
                _units[path] = None
                return None
            raw = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"],
                                 capture_output=True, text=True).stdout.split("\f")
        else:
            raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
        _units[path] = [norm(u) for u in raw]
    return _units[path]


def locate(units: list[str], quote: str, pdf: bool, near: tuple[int, int] | None) -> int | None:
    """1-based line or page where the quote starts, or None if it is not there.
    `near` is the (first, last) unit the evidence names; an occurrence there wins,
    so a quote that also appears earlier in the file is not reported as moved."""
    q = norm(quote)
    if pdf:
        hits = [i + 1 for i, p in enumerate(units) if q in p]
        return next((h for h in hits if near and near[0] <= h <= near[1]), hits[0] if hits else None)
    if q not in " ".join(units):
        return None
    if near:
        lo, hi = max(near[0] - 3, 0), min(near[1] + 2, len(units))
        if q in " ".join(units[lo:hi]):
            return near[0]
    for i in range(len(units)):
        for span in range(1, len(units) - i + 1):
            window = " ".join(units[i:i + span])
            if q in window:
                if q in " ".join(units[i + 1:i + span]):
                    break                     # the quote starts on a later line
                return i + 1
            if len(window) > len(q) + 400:
                break
    return None


def main() -> int:
    text = HTML.read_text(encoding="utf-8")
    tag = '<script id="kg-data" type="application/json">'
    start = text.rindex(tag) + len(tag)
    data = json.loads(text[start:text.index("</script>", start)])
    nodes = data["nodes"]
    ids = [n["id"] for n in nodes]
    by_id = {n["id"]: n for n in nodes}
    clusters = {c["id"] for c in data["clusters"]}
    visuals = set(re.findall(r"^  (\w+)\(n\) \{", text.split("// VISUALS-START")[1]
                             .split("// VISUALS-END")[0], re.M))
    errors, warnings = [], []
    err = errors.append

    for dup in {i for i in ids if ids.count(i) > 1}:
        err(f"duplicate id {dup}")
    linked = set()
    for n in nodes:
        nid = n["id"]
        for f in ("type", "cluster", "title", "summary"):
            if not n.get(f):
                err(f"{nid}: missing {f}")
        if n.get("type") not in TYPES:
            err(f"{nid}: unknown type {n.get('type')}")
        if n.get("cluster") not in clusters:
            err(f"{nid}: unknown cluster {n.get('cluster')}")
        if n.get("status", "current") not in STATUSES:
            err(f"{nid}: unknown status {n.get('status')}")
        if n.get("visual") and n["visual"] not in visuals:
            err(f"{nid}: visual '{n['visual']}' is not defined in the page")
        for link in n.get("links", []):
            if link["to"] not in by_id:
                err(f"{nid}: link to unknown node {link['to']}")
            if link["rel"] not in RELS:
                err(f"{nid}: unknown rel {link['rel']}")
            linked |= {nid, link["to"]}
        prose = " ".join([n.get("summary", "")] + n.get("points", []))
        for ref in re.findall(r"\[\[([^\]|]+)", prose):
            if ref not in by_id:
                err(f"{nid}: [[{ref}]] names no node")

        quoted = 0
        for ev in n.get("evidence", []):
            path = ROOT / ev["file"]
            if ev.get("missing"):
                if path.exists():
                    err(f"{nid}: {ev['file']} now exists -- check whether this item is resolved")
                continue
            if not path.exists():
                err(f"{nid}: evidence file not found: {ev['file']}")
                continue
            if "absent" in ev:
                body = path.read_text(encoding="utf-8", errors="replace").lower()
                for s in [ev["absent"]] if isinstance(ev["absent"], str) else ev["absent"]:
                    if s.lower() in body:
                        err(f"{nid}: '{s}' now appears in {ev['file']} -- check whether "
                            f"this item is resolved")
                continue
            if "quote" not in ev:
                continue
            units = units_of(path)
            if units is None:
                warnings.append(f"{nid}: pdftotext not installed, {ev['file']} not checked")
                quoted += 1
                continue
            pdf = path.suffix == ".pdf"
            want = re.search(r"\b[Lp]\.?(\d+)(?:-(\d+))?", ev.get("loc", ""))
            near = (int(want[1]), int(want[2] or want[1])) if want else None
            at = locate(units, ev["quote"], pdf, near)
            if at is None:
                err(f"{nid}: quote not found in {ev['file']} (source changed?): "
                    f"{ev['quote'][:70]!r}")
                continue
            quoted += 1
            if near:
                lo, hi = near
                slack = 0 if pdf else 2
                if not lo - slack <= at <= hi + slack:
                    unit = "page" if pdf else "line"
                    warnings.append(f"{nid}: quote in {ev['file']} is now at {unit} {at}, "
                                    f"loc says {ev['loc']}")
        if quoted == 0:
            err(f"{nid}: no verified evidence quote")

    for nid in set(ids) - linked:
        err(f"{nid}: not linked to any other node")
    for entry in data.get("changelog", []):
        for key, value in entry.items():
            if key == "removed" or not isinstance(value, list):
                continue
            for nid in value:
                if nid not in by_id:
                    err(f"changelog {entry['date']}: {key} names unknown node {nid}")

    needs = {n["id"]: [l["to"] for l in n.get("links", []) if l["rel"] == "needs"]
             for n in nodes}
    state = {}

    def visit(v, stack):
        state[v] = 1
        for w in needs.get(v, []):
            if state.get(w) == 1:
                err("cycle in needs: " + " -> ".join(stack + [v, w]))
            elif not state.get(w):
                visit(w, stack + [v])
        state[v] = 2

    for v in needs:
        if not state.get(v):
            visit(v, [])

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    count = lambda s: sum(1 for n in nodes if n.get("status", "current") == s)
    print(f"\n{len(nodes)} nodes, {sum(len(n.get('links', [])) for n in nodes)} links, "
          f"{sum(len(n.get('evidence', [])) for n in nodes)} evidence items; "
          f"{count('open')} open, {count('drift')} drift, {count('superseded')} superseded; "
          f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
