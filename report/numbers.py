"""
The few numbers the final report adds to the stage reports. Everything else in the
report is quoted from docs/stage1-report.md, docs/stage2-report.md,
docs/optional-report.md and the run outputs they cite. No API calls.

    uv run python -m report.numbers

Prints:
- the reporter's acceptance rate (proposal §3, step 3: "the acceptance rate is reported"),
  from runs/main/generation_report.json;
- the confidence screen's mean P(truth) at P0, P1 and P2 per judge, mean over cases;
- the top of each judge's stated scale in A1, A3, A4 and A7: its largest P(truth), its
  most common value, and how often it stated 100 (this bounds the independence index);
- mean P(truth) and P(majority) in X1 and X3 per judge, mean over cases, and the share
  of X1's wrong answers that name A's claim;
- right decisions in X2 by the case's quality dimension (not in the table fixed before
  the data: a description);
- mean P(truth) and P(majority) on the wording ladder's rungs, mean over cases;
- the stage 2 comparisons counted over cases, with one-sided sign tests;
- where the abstention arm's conflict-block abstentions fell, by judge, condition and tier,
  and how many X3 trials in T2 cases abstained;
- right decisions from X1 to X3 counted over cases, at both lengths, with one-sided sign
  tests (the table fixed before the data sets no number for an unchanged decision rate);
- 95% intervals from resampling cases: the widest on a mean in each block and on the
  wording ladder, and the A7 - A4 and X1 -> X3 differences the report quotes;
- the main study's judging: trials, tokens and logged cost.
Means over cases use the scorer's cells (pipeline/score.py, `cell`), as tools/tally.py does.
"""

import json
import random
from collections import Counter, defaultdict
from math import comb

from pipeline.score import cell, load

MAIN = "runs/main"
ECHO_IN_SUBSET = {"M3", "M38"}   # the two echo cases among the ten (runs/main/reading-3.4.md)
DRAWS = 10_000                   # resamples of the cases behind each 95% interval
SEED = 4213


def acceptance() -> None:
    gen = json.load(open(f"{MAIN}/generation_report.json"))
    sources = gen["sources"].values()
    cands = [c for s in sources for c in s["candidates"]]
    # a candidate is eligible when it passed every per-candidate check; eligible ones
    # that were not frozen were either too close to an accepted report or not needed
    after = Counter(r.split(" ")[0] for c in cands if not c["accepted"]
                    for r in c["rejected_because"]
                    if r.startswith(("pairwise overlap", "eligible but not needed")))
    not_eligible = [c for c in cands if not c["accepted"] and not any(
        r.startswith(("pairwise overlap", "eligible but not needed"))
        for r in c["rejected_because"])]
    reasons = Counter(r.split(" ")[0] if not r.startswith("cross") else "cross-source"
                      for c in not_eligible for r in c["rejected_because"])
    print(f"reporter: {len(cands)} candidates for {len(gen['sources'])} sources, "
          f"{len(cands) - len(not_eligible)} passed the checks made on each candidate alone, "
          f"{sum(c['accepted'] for c in cands)} frozen, {after['pairwise']} too close to a "
          f"frozen one, {after['eligible']} surplus; "
          f"sources needing a second round: {sum(s['rounds'] > 1 for s in sources)}; "
          f"calls {gen['calls']}")
    print(f"  failed a check: {len(not_eligible)}; by check (a candidate can fail several): "
          + ", ".join(f"{k} {v}" for k, v in reasons.most_common()))


def by_judge_case(path: str, conds: set) -> dict:
    out = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in load(path):
        if r["condition"] in conds:
            out[r["judge_model"].split("/")[-1]][r["case_id"]][r["condition"]].append(r)
    return out


def mean_over_cases(cases: dict, cond: str, key: str) -> float:
    vals = [cell(rs[cond])[key] for rs in cases.values() if cond in rs]
    return sum(vals) / len(vals)


def sign_p(up: int, down: int) -> float:
    """One-sided sign test over cases, as tools/tally.py computes it."""
    n = up + down
    return sum(comb(n, k) for k in range(up, n + 1)) / 2 ** n


def screen() -> None:
    for judge, cases in sorted(by_judge_case(f"{MAIN}/trials-screen.jsonl",
                                             {"P0", "P1", "P2"}).items()):
        print(f"screen {judge}: mean P(truth) over {len(cases)} cases at P0, P1, P2: "
              + ", ".join(f"{mean_over_cases(cases, k, 'p_truth'):.1f}"
                          for k in ("P0", "P1", "P2")))


def scale_top() -> None:
    values = defaultdict(list)
    for r in load(f"{MAIN}/trials-agreement.jsonl"):
        if r["p_truth"] is not None:
            values[(r["judge_model"].split("/")[-1], r["condition"])].append(r["p_truth"])
    for judge in sorted({j for j, _ in values}):
        parts = []
        for cond in ("A1", "A3", "A4", "A7"):
            v = values[(judge, cond)]
            mode, n_mode = Counter(v).most_common(1)[0]
            parts.append(f"{cond} max {max(v):g}, most common {mode:g} ({n_mode}/{len(v)}), "
                         f"100 in {sum(x == 100 for x in v)}")
        print(f"agreement scale {judge}: " + "; ".join(parts))


def conflict() -> None:
    for judge, cases in sorted(by_judge_case(f"{MAIN}/trials-conflict.jsonl",
                                             {"X1", "X3"}).items()):
        wrong = [r for rs in cases.values() for r in rs["X1"] if not r["decision_correct"]]
        on_a = sum(r["forced_choice_decision"] == r["majority_claim"] for r in wrong)
        print(f"conflict {judge}: " + "; ".join(
            f"{k} P(truth) {mean_over_cases(cases, k, 'p_truth'):.1f}, "
            f"P(majority) {mean_over_cases(cases, k, 'p_majority'):.1f}" for k in ("X1", "X3"))
            + f"; X1 wrong answers naming A's claim {on_a}/{len(wrong)}")


def x2_by_dimension() -> None:
    right = defaultdict(lambda: [0, 0])
    for r in load(f"{MAIN}/trials-conflict.jsonl"):
        if r["condition"] == "X2":
            k = (r["judge_model"].split("/")[-1], r["quality_dimension"])
            right[k][0] += bool(r["decision_correct"])
            right[k][1] += 1
    for judge in sorted({j for j, _ in right}):
        print(f"X2 right by dimension {judge}: " + ", ".join(
            f"{d} {right[(judge, d)][0]}/{right[(judge, d)][1]}"
            for d in ("authority", "directness", "method", "primary_source")))


def ladder() -> None:
    for judge, cases in sorted(by_judge_case(f"{MAIN}/trials-ladder.jsonl",
                                             {"W1", "W2", "W3"}).items()):
        print(f"ladder {judge}: " + "; ".join(
            f"{k} P(truth) {mean_over_cases(cases, k, 'p_truth'):.1f}, "
            f"P(majority) {mean_over_cases(cases, k, 'p_majority'):.1f}"
            for k in ("W1", "W2", "W3")))


def stage2_signs() -> None:
    short = by_judge_case(f"{MAIN}/trials-agreement.jsonl", {"A1", "A2"})
    long_ = by_judge_case(f"{MAIN}/trials-long-agreement.jsonl", {"A1", "A2"})
    for judge in sorted(long_):
        for left_out in (set(), ECHO_IN_SUBSET):
            larger = smaller = 0
            for case, rs in long_[judge].items():
                if case in left_out:
                    continue
                rise = lambda d: cell(d["A2"])["p_truth"] - cell(d["A1"])["p_truth"]
                diff = rise(rs) - rise(short[judge][case])
                larger += diff > 0
                smaller += diff < 0
            note = f" without {','.join(sorted(left_out))}" if left_out else ""
            print(f"length {judge}{note}: A1->A2 rise larger at long length in {larger} cases, "
                  f"smaller in {smaller}; one-sided sign test p {sign_p(larger, smaller):.4f}")
    short_x3 = by_judge_case(f"{MAIN}/trials-conflict.jsonl", {"X3"})
    long_x3 = by_judge_case(f"{MAIN}/trials-long-conflict.jsonl", {"X3"})
    for judge in sorted(long_x3):
        n_right = lambda rs: sum(bool(r["decision_correct"]) for r in rs["X3"])
        more = sum(n_right(rs) > n_right(short_x3[judge][c]) for c, rs in long_x3[judge].items())
        fewer = sum(n_right(rs) < n_right(short_x3[judge][c]) for c, rs in long_x3[judge].items())
        print(f"long X3 {judge}: more right decisions than short in {more} cases, fewer in "
              f"{fewer}; one-sided sign test p {sign_p(more, fewer):.4f}")


def abstentions() -> None:
    tiers = Counter()
    x3_t2 = []
    for r in load(f"{MAIN}/trials-abstain.jsonl"):
        if r["abstained"] and r["condition"] in {"X1", "X2", "X3", "X4", "X5"}:
            tiers[(r["judge_model"].split("/")[-1], r["condition"], r["difficulty_tier"])] += 1
        if r["condition"] == "X3" and r["difficulty_tier"] == "T2":
            x3_t2.append(r)
    print("conflict-block abstentions (judge, condition, tier): "
          + (", ".join(f"{k} {v}" for k, v in sorted(tiers.items())) or "none"))
    print(f"abstention arm, X3 in T2 cases: {sum(bool(r['abstained']) for r in x3_t2)} of "
          f"{len(x3_t2)} trials abstained")


def x3_signs() -> None:
    right = lambda rs, k: sum(bool(r["decision_correct"]) for r in rs[k])
    for label, log in (("short", "conflict"), ("long", "long-conflict")):
        for judge, cases in sorted(by_judge_case(f"{MAIN}/trials-{log}.jsonl",
                                                 {"X1", "X3"}).items()):
            more = sum(right(rs, "X3") > right(rs, "X1") for rs in cases.values())
            fewer = sum(right(rs, "X3") < right(rs, "X1") for rs in cases.values())
            print(f"X1->X3 {label} {judge}: right {sum(right(rs, 'X1') for rs in cases.values())}"
                  f" -> {sum(right(rs, 'X3') for rs in cases.values())}; more right in {more} "
                  f"cases, fewer in {fewer}; one-sided sign test p {sign_p(more, fewer):.4f}")


def interval(values: list) -> tuple:
    """The mean, and its 95% percentile interval from resampling the values. Seeded per
    call, so the result does not depend on what ran before it."""
    rng = random.Random(SEED)
    n = len(values)
    means = sorted(sum(rng.choices(values, k=n)) / n for _ in range(DRAWS))
    return sum(values) / n, means[int(0.025 * DRAWS)], means[int(0.975 * DRAWS)]


def widest(figure: str, by_judge: dict, conds: tuple) -> None:
    for judge, cases in sorted(by_judge.items()):
        half = {}
        for k in conds:
            _, low, high = interval([cell(rs[k])["p_truth"] for rs in cases.values()])
            half[k] = (high - low) / 2
        top = max(half, key=half.get)
        print(f"{figure} {judge}: widest 95% interval on a mean +/-{half[top]:.1f} ({top})")


def difference(label: str, by_judge: dict, first: str, second: str) -> None:
    for judge, cases in sorted(by_judge.items()):
        mean, low, high = interval([cell(rs[second])["p_truth"] - cell(rs[first])["p_truth"]
                                    for rs in cases.values()])
        print(f"{label} {judge}: {mean:+.1f}, 95% interval {low:+.1f} to {high:+.1f}")


def intervals() -> None:
    agreement = by_judge_case(f"{MAIN}/trials-agreement.jsonl",
                              {"A1", "A2", "A3", "A4", "A5", "A6", "A7"})
    conflict = by_judge_case(f"{MAIN}/trials-conflict.jsonl", {"X1", "X2", "X3", "X4", "X5"})
    ladder = by_judge_case(f"{MAIN}/trials-ladder.jsonl", {"W1", "W2", "W3"})
    subset = {judge: {case: {**conflict[judge][case], **rs} for case, rs in cases.items()}
              for judge, cases in ladder.items()}
    widest("agreement block", agreement, ("A1", "A2", "A3", "A4", "A5", "A6", "A7"))
    widest("conflict block", conflict, ("X1", "X2", "X3", "X4", "X5"))
    widest("wording ladder", subset, ("X3", "W1", "W2", "W3", "X5"))
    difference("A7 - A4", agreement, "A4", "A7")
    difference("X1 -> X3 rise", conflict, "X1", "X3")


def judging() -> None:
    logs = ("abstain-p0", "abstain", "agreement", "conflict", "screen",
            "ladder", "long-agreement", "long-conflict")
    rows = [r for log in logs for r in load(f"{MAIN}/trials-{log}.jsonl")]
    tokens = sum(r["usage"]["total_tokens"] for r in rows)
    cost = sum(r["usage"]["cost"] for r in rows)
    print(f"main study's judging: {len(rows)} trials, {tokens} tokens, ${cost:.2f}, "
          f"${1000 * cost / len(rows):.2f} per 1,000 trials")


if __name__ == "__main__":
    acceptance()
    screen()
    scale_top()
    conflict()
    x2_by_dimension()
    ladder()
    stage2_signs()
    abstentions()
    x3_signs()
    intervals()
    judging()
