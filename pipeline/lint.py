"""
Static checks on case files, no API calls (proposal §3). Every rule marked [lint] in
docs/authoring-rules.md is checked here; every violation is printed, and the exit code
is non-zero if there is any. R20 (filler length) is a warning only: it never fails.
Set-level counts (tier, dimension, domain) are printed, never asserted. Specificity
asymmetry is NOT checked: no script can see it.

    python -m pipeline.lint                       # the corpus in cases/
    python -m pipeline.lint tests.leaky_cases     # must fail: see tests/test_lint.py
"""

from __future__ import annotations
import importlib
import re
import sys
from collections import Counter

# one implementation of each check, imported, so lint and the pipeline cannot disagree
from pipeline.conditions import LONG_WORDS, base_options
from pipeline.reporter import (CO_OCCURRING_PAIRS, LENGTH_DIFF_MAX, _words, leak_terms,
                               word_ngram_jaccard)

# Matched case-insensitively against A's and B's content, filler and the screen sentence.
LEAK_PATTERNS = {
    "supersession": [
        r"\bmoved to\b", r"\brescheduled\b", r"\bno longer\b", r"\binstead\b",
        r"\bnow\b", r"\boriginal(ly)?\b", r"\bprevious(ly)?\b", r"\bupdated?\b",
        r"\brevis(ed|ion)\b", r"\bincreases? (from|to)\b", r"\bsince\b",
        r"\bsee .* for\b", r"\blater than\b", r"\bextended\b",
    ],
    "staleness": [
        r"\bcached\b", r"\barchived\b", r"\byesterday\b", r"\blast (year|week|month)\b",
        r"\bdays? ago\b", r"\bold(er)?\b", r"\bstale\b", r"\bpre-revision\b",
    ],
    "strong_hearsay": [
        r"\bheard\b", r"\bsomeone (said|told|mentioned)\b", r"\brumou?r\b",
        r"\bsomeone in\b", r"\bsomeone on\b", r"\bapparently\b",
    ],
}
LEAK_RULE = {"supersession": "R1", "staleness": "R3", "strong_hearsay": "R2"}

# R3: dates and recency words. Option strings are removed first, so a date-valued answer
# is not a marker.
TIME_PATTERNS = [
    r"\b(today|tonight|tomorrow|yesterday)\b",
    r"\bthis (morning|afternoon|evening|week|month|term|semester|year)\b",
    r"\b(recent(ly)?|latest|current(ly)?|newly|as of)\b",
    r"\b(january|february|march|april|june|july|august|september|october|"
    r"november|december)\b",
    r"\b(19|20)\d\d\b",
]
# R2: attribution in content or filler says who produced the information.
ATTRIBUTION_PATTERNS = [
    r"\baccording to\b", r"\b(un)?official(ly)?\b",
    r"\b(confirmed|verified|reportedly|allegedly)\b",
]
# R10: filler that describes its own document, or drifts out of plain register
# (second person would grow a register cue with report length).
DOC_TYPE_PATTERNS = [
    r"\b(this|the following) (announcement|notice|document|page|table|email|"
    r"message|post|brief|schedule|timetable|memo|sheet|wiki|list)\b",
    r"\b(rows?|columns?)\b",
]
REGISTER_PATTERNS = [r"\byou(r|rs|rself)?\b"]
PROVENANCE_KEYS = ("type", "authority", "why")
R17_MAX = 0.40   # content bigram overlap of co-occurring sources must be BELOW this
PARAPHRASES_NEEDED = {"A": 2, "B": 3, "C": 1, "D": 1}   # R14


def _mentions(text: str, value: str) -> bool:
    """`value` appears in `text` as a whole token ("10%" not inside "110%")."""
    return re.search(rf"(?<![\w.]){re.escape(value)}(?![\w])", text, re.I) is not None


def _first(patterns: list[str], text: str) -> str | None:
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return m.group(0)
    return None


def lint_case(case: dict) -> list[tuple[str, str]]:
    """Every violation in one case, as (rule, message)."""
    v = []
    srcs = case.get("sources", {})
    if sorted(srcs) != ["A", "B", "C", "D"]:
        return [("schema", f"sources must be exactly A-D, got {sorted(srcs)}")]

    # R5 / R8: options are built from the truth, A's claim and exactly two distractors
    if "answer_options" in case:
        v.append(("R5", "answer_options is authored; it must be built from truth, "
                        "A's claim and the distractors"))
    n_dist = len(case.get("distractors", []))
    if n_dist != 2:
        v.append(("R8", f"a case needs exactly 2 distractors, has {n_dist}"))
    opts = base_options(case)
    if len(set(opts)) != len(opts):
        v.append(("R8", f"options are not distinct (truth, A's claim, distractors): {opts}"))
    wrong = [k for k, s in srcs.items() if s["claim"] != case["world_truth"]]
    if wrong != ["A"]:
        v.append(("one-wrong", f"exactly one source (A) must support a wrong answer; wrong: {wrong}"))

    # R14: the shared source is always B; A appears only in the conflict block
    got_n = {k: s.get("n_paraphrases_needed") for k, s in srcs.items()}
    if got_n != PARAPHRASES_NEEDED:
        v.append(("R14", f"n_paraphrases_needed must be {PARAPHRASES_NEEDED}, got {got_n}"))

    # R17: co-occurring sources use different sentence frames, checked before generation
    # -- near-identical sources give near-identical paraphrases
    for a, b in CO_OCCURRING_PAIRS:
        o = word_ngram_jaccard(srcs[a].get("content", ""), srcs[b].get("content", ""))
        if o >= R17_MAX:
            v.append(("R17", f"{a}/{b} content overlap {o:.2f} >= {R17_MAX}: co-occurring "
                             f"sources must use different sentence frames"))

    # R2 / R12: schema of each source
    for key, s in srcs.items():
        prov = s.get("provenance", {})
        missing = [k for k in PROVENANCE_KEYS if not prov.get(k)]
        if missing or "content" not in s or "text" in s:
            v.append(("R2", f"{key}: needs `content` and provenance {PROVENANCE_KEYS}, "
                            f"no colon-header `text`; missing {missing}"))
        if prov.get("quality") not in (None, s.get("quality")):
            v.append(("R2", f"{key}: provenance quality {prov['quality']!r} != source quality {s.get('quality')!r}"))
        if "filler" in s:
            v.append(("R12", f"{key}: filler attached to a source; it belongs to the report slot"))

    sets = case.get("filler_sets", [])
    if len(sets) != 3 or not all(isinstance(fs, list) and fs and all(isinstance(x, str) for x in fs)
                                 for fs in sets):
        v.append(("R12", f"filler_sets must be three non-empty lists of sentences, got {len(sets)}"))
    seen = {}
    for i, fs in enumerate(sets):
        for sent in fs:
            if sent in seen and seen[sent] != i:
                v.append(("R12", f"sets {seen[sent]} and {i} share a sentence: {sent[:60]!r}"))
            seen.setdefault(sent, i)
    filler = [(f"filler[{i}]", sent) for i, fs in enumerate(sets) for sent in fs]
    contents = [(f"{k}/content", s.get("content", "")) for k, s in srcs.items()]

    # R8b / R9: distractors nowhere; truth and A's claim not in filler
    for d in case.get("distractors", []):
        for key, s in srcs.items():
            where = [("claim", s["claim"]), ("content", s.get("content", ""))] + \
                    [(f"provenance.{k}", str(x)) for k, x in s.get("provenance", {}).items()]
            for field, text in where:
                if _mentions(text, d):
                    v.append(("R8b", f"distractor {d!r} named in {key}/{field}"))
        for where, sent in filler:
            if _mentions(sent, d):
                v.append(("R9", f"distractor {d!r} named in {where}"))
    for opt in opts[:2]:
        for where, sent in filler:
            if _mentions(sent, opt):
                v.append(("R9", f"option {opt!r} named in {where}"))

    # R15: the screen sentence. It is NOT a source, so R8 and R9 (which it exists to
    # break: P1 rules out two options) are never applied to it; R1-R3, R10, R11 and R13
    # are, below, because a judge still reads it.
    screen = case.get("screen_partial")
    if not isinstance(screen, str) or not screen.strip():
        v.append(("R15", "screen_partial is missing: one sentence for screen level P1"))
        screen = None
    screen_only = [("screen_partial", screen)] if screen else []

    # R1 / R2 / R3 / R10 patterns
    def strip_opts(text):
        for o in opts:
            text = re.sub(rf"(?<![\w.]){re.escape(o)}(?![\w])", " ", text, flags=re.I)
        return text
    ab = [(w, t) for w, t in contents if w[0] in "AB"]
    for where, text in ab + filler + screen_only:
        for kind, pats in LEAK_PATTERNS.items():
            hit = _first(pats, text)
            if hit:
                v.append((LEAK_RULE[kind], f"{kind} {hit!r} in {where}: {text[:70]!r}"))
        hit = _first(ATTRIBUTION_PATTERNS, text)
        if hit:
            v.append(("R2", f"attribution {hit!r} in {where}: {text[:70]!r}"))
    for where, text in contents + filler + screen_only:
        hit = _first(TIME_PATTERNS, strip_opts(text))
        if hit:
            v.append(("R3", f"time marker {hit!r} in {where}: {text[:70]!r}"))
    for where, text in filler + screen_only:
        hit = _first(DOC_TYPE_PATTERNS, text) or _first(REGISTER_PATTERNS, text)
        if hit:
            v.append(("R10", f"document-type or register word {hit!r} in {where}: {text[:70]!r}"))

    # R11: one operative sentence
    for where, text in contents + screen_only:
        t = text.strip()
        if not re.search(r"[.!?]$", t) or re.search(r"[.!?]\s+\S", t):
            v.append(("R11", f"{where} is not exactly one sentence: {t!r}"))

    # R13: A and B share exactly the same set of question content-words. A word both use
    # is symmetric and harmless; one used by only one of them fails here.
    q = _words(case.get("question", ""))
    qa, qb = q & _words(srcs["A"].get("content", "")), q & _words(srcs["B"].get("content", ""))
    if qa != qb:
        v.append(("R13", f"question words differ between the competing pair: "
                         f"A only {sorted(qa - qb)}, B only {sorted(qb - qa)}"))
    return v


def r13_notes(case: dict) -> list[str]:
    """R13's printed-not-enforced part: question words in some of B, C, D only."""
    q = _words(case.get("question", ""))
    per_src = {k: _words(case["sources"][k].get("content", "")) for k in "BCD"}
    return [f"question word {w!r} in {[k for k in 'BCD' if w in per_src[k]]} only"
            for w in sorted(q) if 0 < sum(w in per_src[k] for k in "BCD") < 3]


def length_notes(case: dict) -> list[str]:
    """R20, printed, not enforced: a long report is one filler set plus a paraphrase of
    A or B (the only sources the length arm uses), and must land in the 88-96-word band
    (docs/decisions.md). An accepted paraphrase is within LENGTH_DIFF_MAX words of its
    source, so the set plus each source sentence must sit that far inside the band
    (91-93) for every accepted paraphrase to fit. The real reports are checked when the
    length arm is built."""
    lo, hi = LONG_WORDS[0] + LENGTH_DIFF_MAX, LONG_WORDS[1] - LENGTH_DIFF_MAX
    srcs = case.get("sources", {})
    sizes = {k: len(srcs[k].get("content", "").split()) for k in "AB" if k in srcs}
    if not sizes:
        return []
    notes = []
    spread = max(sizes.values()) - min(sizes.values())
    if spread > hi - lo:
        notes.append(f"A's and B's sentences are {sizes.get('A')} and {sizes.get('B')} words; "
                     f"keep them within {hi - lo} words of each other, or no filler set fits")
    for i, fs in enumerate(case.get("filler_sets", [])):
        n = sum(len(sent.split()) for sent in fs)
        if n + min(sizes.values()) < lo or n + max(sizes.values()) > hi:
            notes.append(f"filler_sets[{i}] is {n} words; with A's and B's sentences its long "
                         f"reports are {n + min(sizes.values())}-{n + max(sizes.values())} "
                         f"words, outside {lo}-{hi}, so a rewording up to {LENGTH_DIFF_MAX} "
                         f"words off could leave {LONG_WORDS[0]}-{LONG_WORDS[1]}")
    return notes


def lint(cases: dict) -> list[tuple[str, str, str]]:
    """Prints every violation and the set-level counts; returns (case, rule, message)."""
    out = []
    for cid, case in cases.items():
        for rule, msg in lint_case(case):
            out.append((cid, rule, msg))
            print(f"  [{cid}] {rule:9s} {msg}")
        if sorted(case.get("sources", {})) == ["A", "B", "C", "D"]:
            for note in r13_notes(case):
                print(f"  [{cid}] R13 note (not enforced): {note}")
        for note in length_notes(case):
            print(f"  [{cid}] R20 warning (not enforced): {note}")
        for key, src in case.get("sources", {}).items():
            if src.get("provenance", {}).get("type") and "content" in src:
                terms = leak_terms(src, case["question"])
                print(f"  [{cid}/{key}] provenance-only terms policed in reports: {sorted(terms)}")

    print(f"\n{len(out)} violation(s) across {len(cases)} case(s).\n")
    # Printed, never asserted. No position balance: option order is the builder's
    # rotation, not a corpus property.
    print("Set-level counts:")
    for label, key in [("difficulty tier", "difficulty_tier"),
                       ("quality dimension", "quality_dimension"), ("domain", "domain")]:
        print(f"  {label:18s} : {dict(Counter(str(c.get(key, 'n/a')) for c in cases.values()))}")
    return out


if __name__ == "__main__":
    modname = sys.argv[1] if len(sys.argv) > 1 else "cases"
    cases = importlib.import_module(modname.removesuffix(".py").replace("/", ".")).CASES
    print(f"== {modname} ==")
    sys.exit(1 if lint(cases) else 0)
