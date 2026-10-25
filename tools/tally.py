"""
Across-case tallies for reading a run against the README's table "What counts as
support, fixed before any data". The scorer prints every cell per judge and case; this
prints, per judge, the counts and means over cases that the table's rows ask about. It
reads the same trial logs and reuses the scorer's cells and n_eff, so its numbers match
the scorer's tables. It describes; the table decides. No API calls.

    uv run python -m tools.tally runs/main/trials-*.jsonl
    uv run python -m tools.tally --without M3,M9 runs/main/trials-*.jsonl   # leave cases out
    uv run python -m tools.tally --only M4,M5 runs/main/trials-*.jsonl      # keep only these

n_eff counts only for judges the confidence screen keeps: see the scorer's SCREEN lines.
"""

import statistics
import sys
from collections import defaultdict
from math import comb

from pipeline.conditions import AGREEMENT_BLOCK, CONFLICT_BLOCK
from pipeline.score import cell, load, neff


def _mean(xs) -> float:
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs)


def _sign_p(up: int, down: int) -> float:
    """One-sided sign test over cases: the chance of at least `up` gains among the
    up + down cases that changed, if a gain and a loss were equally likely."""
    n = up + down
    return sum(comb(n, k) for k in range(up, n + 1)) / 2 ** n


def tally(records: list[dict]) -> None:
    by = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))  # judge, case, cond
    case_info = {}
    for r in records:
        if r["arm"] == "short":
            by[r["judge_model"]][r["case_id"]][r["condition"]].append(r)
            case_info[r["case_id"]] = (r["domain"], r["difficulty_tier"])
    for judge, cases in sorted(by.items()):
        ids = sorted(cases, key=lambda c: int(c[1:]))
        cells = {c: {k: cell(rs) for k, rs in cases[c].items()} for c in ids}
        pt = lambda c, k: cells[c][k]["p_truth"]
        print(f"== judge {judge} ({len(ids)} cases)")

        def right(k, which=ids, keep=lambda r: True):
            rs = [r for c in which for r in cases[c][k] if keep(r)]
            return f"{sum(bool(r['decision_correct']) for r in rs)}/{len(rs)}"

        print("agreement, mean P(truth) over cases: " +
              ", ".join(f"{k} {_mean(pt(c, k) for c in ids):.1f}" for k in AGREEMENT_BLOCK))
        up = [c for c in ids if pt(c, "A4") > pt(c, "A1")]
        down = [c for c in ids if pt(c, "A4") < pt(c, "A1")]
        domains = defaultdict(lambda: [0, 0])
        for c in ids:
            domains[case_info[c][0]][0] += c in up
            domains[case_info[c][0]][1] += 1
        # the truth's position among the shown options is the option rotation
        at = lambda k, pos: _mean(r["p_truth"] for c in ids for r in cases[c][k]
                                  if r["option_rotation"] == pos)
        positions = sorted({r["option_rotation"] for c in ids for r in cases[c]["A1"]})
        print(f"H1 A1 -> A4: P(truth) rises in {len(up)}/{len(ids)} cases, falls in "
              f"{len(down)}; by domain: " +
              ", ".join(f"{d} {a}/{n}" for d, (a, n) in sorted(domains.items())) +
              "; by the truth's position: " +
              ", ".join(f"{p + 1}: {at('A1', p):.1f} -> {at('A4', p):.1f}" for p in positions))
        # in A4 one source fills every slot; in X1 the strong report's slot rotates
        slots = sorted({r["indep_slot"] for c in ids for r in cases[c]["X1"]})
        print("H1 X1, right decisions by the strong report's position: " +
              ", ".join(f"{s + 1}: {right('X1', keep=lambda r, s=s: r['indep_slot'] == s)}"
                        for s in slots))
        print(f"H2: A3 above A2 in {sum(pt(c, 'A3') > pt(c, 'A2') for c in ids)}/{len(ids)} "
              f"cases, A4 above A2 in {sum(pt(c, 'A4') > pt(c, 'A2') for c in ids)}; mean "
              f"|A4 - A3| {_mean(abs(pt(c, 'A4') - pt(c, 'A3')) for c in ids):.1f}; mean "
              f"A7 - A4 {_mean(pt(c, 'A7') - pt(c, 'A4') for c in ids):+.1f}")

        values = [neff(cells[c]) for c in ids]
        medians = []
        for k in ("A4", "A6", "A7", "CN", "IS", "RP"):
            got = [v[k] for v in values if isinstance(v.get(k), (int, float))]
            medians.append(f"{k} {statistics.median(got):.2f} (n={len(got)})" if got
                           else f"{k} none")
        print("n_eff, median over the cases with a value (normative A4 1, A6 1, A7 3): " +
              ", ".join(medians) + f"; undefined in {sum('undefined' in v for v in values)}, "
              f"a value at ceiling in {sum('at ceiling' in v.values() for v in values)}")

        print("conflict, right decisions and mean P(truth): " +
              ", ".join(f"{k} {right(k)} {_mean(pt(c, k) for c in ids):.1f}"
                        for k in CONFLICT_BLOCK))
        tiers = {t: [c for c in ids if case_info[c][1] == t] for t in ("T1", "T2")}
        print(f"H3 X1 -> X3: P(truth) rises in {sum(pt(c, 'X3') > pt(c, 'X1') for c in ids)}"
              f"/{len(ids)} cases; by tier, right decisions and mean P(truth): " +
              "; ".join(f"{t} {right('X1', cs)} -> {right('X3', cs)}, "
                        f"{_mean(pt(c, 'X1') for c in cs):.1f} -> "
                        f"{_mean(pt(c, 'X3') for c in cs):.1f}"
                        for t, cs in tiers.items() if cs))
        more = sum(cells[c]["X2"]["correct"] > cells[c]["X1"]["correct"] for c in ids)
        fewer = sum(cells[c]["X2"]["correct"] < cells[c]["X1"]["correct"] for c in ids)
        print(f"H5 X1 -> X2: more right decisions in {more}/{len(ids)} cases, fewer in "
              f"{fewer}; one-sided sign test p {_sign_p(more, fewer):.4f}")
        print()


if __name__ == "__main__":
    args, drop, only = sys.argv[1:], set(), set()
    while args[:1] in (["--without"], ["--only"]):
        (drop if args[0] == "--without" else only).update(args[1].split(","))
        args = args[2:]
    order = lambda ids: ", ".join(sorted(ids, key=lambda c: int(c[1:])))
    print(f"cases left out: {order(drop) or 'none'}"
          + (f"; only these kept: {order(only)}" if only else "") + "\n")
    tally([r for path in args for r in load(path)
           if r["case_id"] not in drop and (not only or r["case_id"] in only)])
