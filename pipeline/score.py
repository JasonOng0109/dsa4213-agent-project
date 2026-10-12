"""
The scorer: reads a JSONL trial log and prints, per judge, arm and case, a table of
every cell and the comparisons the proposal pre-registers (§5), then the confidence
screen, the independence index n_eff, and run health.

Cells are judge x arm x case x condition. Comparisons find their cells by factor
vector, never by condition name. Every comparison is reported per judge before any
pooling.

    python -m pipeline.score runs/trials.jsonl
"""

from __future__ import annotations
import json
import math
from collections import Counter, defaultdict

from pipeline.judge import PARSE_FAILURES

ORDER = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "X1", "X2", "X3", "X4", "X5",
         "W1", "W2", "W3", "P0", "P1", "P2"]
SCREEN = ["irrelevant", "partial", "determinate"]   # P0 < P1 < P2 in stated P(truth)
# the conflict block's hub: nothing, dependence, quality, both -- all on the 2-vs-1
# conflict with no source names shown
PRIMARY = [("X1", False, False), ("X3", True, False), ("X4", False, True), ("X5", True, True)]


def load(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 1) if xs else None


def stability(rs: list[dict]) -> tuple:
    """Measure 2: the proportion of a cell's repeats returning the most common answer,
    over the repeats that parsed. 1.0 when every repeat agrees. An abstention is its own
    answer value, not missing, so a judge that abstains consistently scores high -- the
    correct reading. Returns (proportion, repeats used): the count is not optional, since
    stability over 4 and over 12 repeats are not comparable."""
    ok = [r for r in rs if r["parsing_status"] not in PARSE_FAILURES]
    if not ok:
        return None, 0
    votes = Counter("<abstain>" if r["abstained"] else r["forced_choice_decision"] for r in ok)
    return round(max(votes.values()) / len(ok), 2), len(ok)


def cell(rs: list[dict]) -> dict:
    """One judge x arm x case x condition cell. Rates are over the repeats that parsed:
    a parse failure is excluded from decision denominators, never counted as wrong
    (proposal §3). An abstention or an off-list answer (no_match) stays in."""
    n = len(rs)
    n_fail = sum(1 for r in rs if r["parsing_status"] in PARSE_FAILURES)
    valid = n - n_fail
    rate = lambda hit: sum(1 for r in rs if hit(r)) / valid if valid else None
    stab, n_stab = stability(rs)
    return {
        "n": n,
        "correct": rate(lambda r: r["decision_correct"]),
        "abstain": rate(lambda r: r["abstained"]),
        "no_match": rate(lambda r: r["parsing_status"] == "no_match"),
        "parse_fail": n_fail,
        "p_truth": _mean(r["p_truth"] for r in rs),
        "p_majority": _mean(r["p_majority"] for r in rs),
        # top stated probability minus second: indifference, which coherence cannot see
        "margin": _mean(r.get("margin") for r in rs),
        "stability": stab,
        "n_stability": n_stab,
        "chance": 1 / len(rs[0]["answer_options"]),
        "factors": rs[0]["factors"],
    }


def _rate(x) -> str:
    return "n/a" if x is None else f"{x:.2f}"


def _by_factor(cells: dict, **want) -> dict | None:
    hits = [c for c in cells.values() if all(c["factors"].get(k) == v for k, v in want.items())]
    return hits[0] if len(hits) == 1 else None


def main(path: str) -> None:
    report(load(path))


def report(records: list[dict]) -> None:
    status = Counter(r["parsing_status"] for r in records)
    n_fail = sum(status.get(s, 0) for s in PARSE_FAILURES)
    print(f"Loaded {len(records)} trials. Parse failures: {n_fail}. "
          f"Status counts: {dict(status)}\n")
    groups = defaultdict(lambda: defaultdict(list))
    for r in records:
        groups[(r["judge_model"], r["arm"], r["case_id"])][r["condition"]].append(r)
    screen = defaultdict(dict)     # judge -> case -> [P(truth) at P0, P1, P2]
    for (judge, arm, case_id), conds in sorted(groups.items()):
        cells = {c: cell(rs) for c, rs in conds.items()}
        abst = arm == "abstain"
        print(f"##### judge {judge} | arm {arm} | {case_id} #####")
        print(f"  {'cond':4s} {'n':>3s} {'chance':>6s} {'correct':>7s} {'abstain':>7s} "
              f"{'no_match':>8s} {'P(truth)':>8s} {'P(maj)':>6s} {'margin':>6s} {'stab':>11s}")
        for c in sorted(cells, key=ORDER.index):
            x = cells[c]
            stab = ("n/a" if x["stability"] is None
                    else f"{x['stability']:.2f}(n={x['n_stability']})")
            print(f"  {c:4s} {x['n']:3d} {x['chance']:6.2f} {_rate(x['correct']):>7s} "
                  f"{_rate(x['abstain']):>7s} {_rate(x['no_match']):>8s} {str(x['p_truth']):>8s} "
                  f"{str(x['p_majority']):>6s} {str(x['margin']):>6s} {stab:>11s}"
                  + (f"  PARSE FAIL x{x['parse_fail']}" if x["parse_fail"] else ""))
        ladder = [(name, _by_factor(cells, conflict="2-vs-1", provenance_shown="none",
                                    dependence_stated=d, quality_stated=q))
                  for name, d, q in PRIMARY]
        if arm == "screen":
            screen[judge][case_id] = [
                (_by_factor(cells, informativeness=lvl) or {}).get("p_truth") for lvl in SCREEN]
        if all(c for _, c in ladder):
            print("  -- X1 -> X3 -> X4 -> X5 (none, dependence, quality, both) --")
            for key in ("correct", "p_truth", "p_majority") + (("abstain",) if abst else ()):
                is_rate = key in ("correct", "abstain")
                print(f"  {key:10s}: " + " -> ".join(
                    _rate(c[key]) if is_rate else str(c[key]) for _, c in ladder))
            baseline = _by_factor(cells, conflict="no", sources=3)
            if abst and baseline and baseline["abstain"] is not None:
                # within judge only, against this judge's own no-conflict cell, A7:
                # propensity to abstain varies widely between models
                base = baseline["abstain"]
                print(f"  abstain delta vs own A7 ({base:.2f}): "
                      + ", ".join(f"{n} {c['abstain'] - base:+.2f}" for n, c in ladder
                                  if c["abstain"] is not None))
        print()

    excluded = set()
    for judge, by_case in sorted(screen.items()):
        verdict, detail = screen_verdict(by_case)
        print(f"SCREEN judge {judge}: P(truth) at P0, P1, P2 -- {detail} -- {verdict}")
        if verdict == "EXCLUDED":
            excluded.add(judge)
    print()
    report_neff(records, excluded)
    report_health(records)


def _logit(p: float) -> float:
    p = min(0.99, max(0.01, p))          # clip before the logit
    return math.log(p / (1 - p))


def neff(cells: dict) -> dict:
    """n_eff(c) = (l(c) - l(A0)) / (l(A1) - l(A0)), l = logit of the cell's mean stated
    P(truth) on the short arm (proposal §4.2). Undefined when |w| < 0.2 logits, and an
    anomaly when w is negative: the repeated source supports the truth, so a judge whose
    belief in it falls after one report has a backwards unit, and every value derived
    from it would invert. Returns the values plus CN (correlation neglect), IS
    (independence sensitivity), RP (repair from disclosure) and how many cells were
    clipped."""
    need = ["A0", "A1", "A4", "A6", "A7"]
    if any(cells.get(c) is None or cells[c].get("p_truth") is None for c in need):
        return {"undefined": "missing P(truth) in " + str([c for c in need if not cells.get(c)])}
    p = {c: cells[c]["p_truth"] / 100 for c in need}
    clipped = sum(1 for v in p.values() if not 0.01 <= v <= 0.99)
    l = {c: _logit(v) for c, v in p.items()}
    w = l["A1"] - l["A0"]
    if abs(w) < 0.2:
        return {"undefined": f"w = l(A1) - l(A0) = {w:.3f} < 0.2 logits", "clipped": clipped}
    if w < 0:
        return {"undefined": f"anomaly: w = l(A1) - l(A0) = {w:.3f} is negative, one "
                             f"supporting report lowered belief in the truth",
                "anomaly": True, "clipped": clipped}
    n = {c: round((l[c] - l["A0"]) / w, 2) for c in ("A4", "A6", "A7")}
    return dict(n, w=round(w, 3), clipped=clipped, CN=round(n["A4"] - 1, 2),
                IS=round(n["A7"] - n["A4"], 2), RP=round(n["A4"] - n["A6"], 2))


def report_neff(records: list[dict], excluded: set = frozenset()) -> None:
    """n_eff only for judges the confidence screen retains: a judge whose stated numbers
    do not order has no usable scale, so its n_eff is undefined even when the arithmetic
    would run. The undefined rate is itself reported per judge."""
    groups = defaultdict(lambda: defaultdict(list))
    for r in records:
        if r["arm"] == "short":
            groups[(r["judge_model"], r["case_id"])][r["condition"]].append(r)
    undefined = defaultdict(list)          # judge -> one bool per case
    for (judge, case_id), conds in sorted(groups.items()):
        cells = {c: cell(rs) for c, rs in conds.items()}
        pt = {c: cells[c]["p_truth"] for c in ("A0", "A1", "A4", "A6", "A7") if c in cells}
        value = ({"undefined": "judge failed the confidence screen"} if judge in excluded
                 else neff(cells))
        undefined[judge].append("undefined" in value)
        print(f"N_EFF judge {judge} | {case_id}: mean P(truth) {pt} -> {value}  "
              f"(normative A4 1, A6 1, A7 3)")
    for judge, flags in sorted(undefined.items()):
        print(f"N_EFF UNDEFINED judge {judge}: {sum(flags)}/{len(flags)} cells "
              f"({sum(flags) / len(flags):.2f})")
    print()


def report_health(records: list[dict]) -> None:
    by_judge = defaultdict(list)
    for r in records:
        by_judge[r["judge_model"]].append(r)
    for judge, rs in sorted(by_judge.items()):
        fails = sum(r["parsing_status"] in PARSE_FAILURES for r in rs)
        nomatch = sum(r["parsing_status"] == "no_match" for r in rs)
        other = sorted({r["parsing_status"] for r in rs} - {"ok", "no_match", *PARSE_FAILURES})
        provs = sorted({str(r.get("serving_provider")) for r in rs})
        reason = sum(r.get("reasoning_tokens") or 0 for r in rs)
        errors = sum(1 for r in rs if r.get("call_error"))
        print(f"HEALTH judge {judge}: {len(rs)} trials, parse failures {fails}, no_match "
              f"{nomatch}, other statuses {other}, call errors {errors}, providers {provs}, "
              f"reasoning tokens {reason}")
        costs = defaultdict(list)
        for r in rs:
            c = (r.get("usage") or {}).get("cost")
            if c is not None:
                costs[r["arm"]].append(c)
        if costs:
            print("  cost per call by arm: " + ", ".join(
                f"{a} ${sum(v) / len(v):.5f} (n={len(v)}, total ${sum(v):.4f})"
                for a, v in sorted(costs.items())))
    # which cells each judge reasoned in is a result, not a footnote
    rt = defaultdict(lambda: defaultdict(list))
    for r in records:
        if r.get("reasoning_tokens") is not None:
            rt[r["judge_model"]][(r["arm"], r["condition"])].append(r["reasoning_tokens"])
    for judge, cells in sorted(rt.items()):
        hot = {f"{a}/{c}": f"{sum(t > 0 for t in v)}/{len(v)} trials, mean {sum(v) / len(v):.0f}"
               for (a, c), v in sorted(cells.items()) if any(v)}
        print(f"REASONING judge {judge}: " + (str(hot) if hot else "0 reasoning tokens in every cell"))
    inc = [r for r in records if r.get("coherent") is False]
    print(f"\nINCOHERENT records (answer is not the argmax of its own p): {len(inc)}")
    for r in inc:
        print(f"  {r['trial_id']} {r['judge_model']} options={r['answer_options']} "
              f"raw={r['raw_judge_output']}")


def screen_verdict(by_case: dict) -> tuple[str, str]:
    """Ordering check: per case, stated P(truth) (mean over the option rotations) must
    strictly increase P0 < P1 < P2 on the judge's own scale; absolute values are not
    scored. The judge is EXCLUDED from probability-based analyses only if it fails on
    more than a third of cases; per-case detail is always shown."""
    passed = {cid: None not in v and v[0] < v[1] < v[2] for cid, v in by_case.items()}
    n_fail = sum(not ok for ok in passed.values())
    detail = "; ".join(f"{cid} {' < '.join(str(x) for x in v)} {'PASS' if passed[cid] else 'FAIL'}"
                       for cid, v in sorted(by_case.items()))
    verdict = "EXCLUDED" if n_fail * 3 > len(passed) else "retained"
    return verdict, f"{detail} ({n_fail}/{len(passed)} failed)"


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
