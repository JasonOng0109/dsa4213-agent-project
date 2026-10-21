"""
The scorer: reads a JSONL trial log and prints, per judge, arm and case, a table of
every cell and the comparisons the proposal pre-registers (§5), then the confidence
screen (ordering), the discrimination check, the independence index n_eff, H6's test,
and run health.

Cells are judge x arm x case x condition. Comparisons find their cells by factor
vector, never by condition name. Every comparison is reported per judge before any
pooling.

    python -m pipeline.score runs/trials.jsonl [more logs ...]
    python -m pipeline.score --show-excluded runs/trials-*.jsonl      # the pilot

Several logs (for example from staged runs) are scored together. `--show-excluded` also
prints n_eff and H6 for the judges the confidence screen excludes, marked as checks, not
results. It was added for the pilot, where discrimination, then part of the screen,
excluded all three judges; since 2026-10-21 only ordering excludes (docs/decisions.md).
"""

from __future__ import annotations
import json
import math
import random
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations

from pipeline.conditions import AGREEMENT_BLOCK, CONFLICT_BLOCK, LADDER
from pipeline.judge import PARSE_FAILURES

ORDER = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "X1", "X2", "X3", "X4", "X5",
         "W1", "W2", "W3", "P0", "P1", "P2"]
SCREEN = ["irrelevant", "partial", "determinate"]   # P0 < P1 < P2 in stated P(truth)
SCREEN_ALPHA = 0.05     # one-sided; the proposal names no level, the team fixed this one
MIN_CLASS = 10          # discrimination counts a condition with this many correct and incorrect
SHUFFLES = 2000         # discrimination's p-value: this many shuffles of whole cases ...
SHUFFLE_SEED = 0        # ... from a fixed seed, so the same log always gives the same p
# H6: a top-two margin below this many points is near indifference; the sensitivity
# cut-offs are printed beside it, declared in advance (team decisions, 2026-10-18)
MARGIN_THRESHOLD = 10
MARGIN_SENSITIVITY = (5, 20)
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


@lru_cache(maxsize=None)
def stability_chance(n: int, k: int = 4) -> float:
    """Expected stability under random answering: the mean share of the most common of k
    equally likely answers over n repeats. Not 1/k, because the measure takes the largest
    of k counts (proposal §5): about 0.53 at 4 repeats, 0.47 at 6 and 0.41 at 12.
    Computed exactly, over every way n answers can split across k values."""
    def splits(n, k):
        if k == 1:
            yield (n,)
            return
        for i in range(n + 1):
            for rest in splits(n - i, k - 1):
                yield (i,) + rest
    total = 0
    for counts in splits(n, k):
        ways = math.factorial(n)
        for c in counts:
            ways //= math.factorial(c)
        total += ways * max(counts)
    return total / k ** n / n


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
        # random answering over every possible answer value, abstention included if offered
        "stability_chance": (round(stability_chance(n_stab, len(rs[0]["answer_options"])
                                                    + bool(rs[0].get("allow_abstain"))), 2)
                             if n_stab else None),
        "chance": 1 / len(rs[0]["answer_options"]),
        "factors": rs[0]["factors"],
    }


def _rate(x) -> str:
    return "n/a" if x is None else f"{x:.2f}"


def _by_factor(cells: dict, **want) -> dict | None:
    hits = [c for c in cells.values() if all(c["factors"].get(k) == v for k, v in want.items())]
    return hits[0] if len(hits) == 1 else None


def main(*args: str) -> None:
    """Score every log named; `--show-excluded` is explained in the module docstring."""
    paths = [a for a in args if a != "--show-excluded"]
    report([r for p in paths for r in load(p)], show_excluded="--show-excluded" in args)


def report(records: list[dict], show_excluded: bool = False) -> None:
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
              f"{'no_match':>8s} {'P(truth)':>8s} {'P(maj)':>6s} {'margin':>6s} {'stab':>11s} "
              f"{'s_chance':>8s}")
        for c in sorted(cells, key=ORDER.index):
            x = cells[c]
            stab = ("n/a" if x["stability"] is None
                    else f"{x['stability']:.2f}(n={x['n_stability']})")
            print(f"  {c:4s} {x['n']:3d} {x['chance']:6.2f} {_rate(x['correct']):>7s} "
                  f"{_rate(x['abstain']):>7s} {_rate(x['no_match']):>8s} {str(x['p_truth']):>8s} "
                  f"{str(x['p_majority']):>6s} {str(x['margin']):>6s} {stab:>11s} "
                  f"{_rate(x['stability_chance']):>8s}"
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

    report_ladder(records)
    excluded = set()
    for judge, by_case in sorted(screen.items()):
        verdict, detail = screen_verdict(by_case)
        print(f"SCREEN judge {judge}: P(truth) at P0, P1, P2 -- {detail} -- {verdict}")
        if verdict == "EXCLUDED":
            excluded.add(judge)
    print()
    report_discrimination(records)
    report_neff(records, excluded, show_excluded)
    report_h6(records, excluded, show_excluded)
    report_health(records)


def report_ladder(records: list[dict]) -> None:
    """H4's defence against compliance (proposal §4.1): decisions up the graded wording
    ladder, from the weakest rung to X5's categorical wording as the ceiling. If weaker
    wordings also move decisions, the judge is weighing evidence; if only the strongest
    does, it is complying with an instruction."""
    groups = defaultdict(lambda: defaultdict(list))
    for r in records:
        if r["arm"] == "ladder" or (r["arm"] == "short" and r["condition"] == "X5"):
            groups[(r["judge_model"], r["case_id"])][r["condition"]].append(r)
    for (judge, case_id), conds in sorted(groups.items()):
        if not any(c in conds for c in LADDER):
            continue
        steps = [(c, cell(conds[c])) for c in LADDER + ["X5"] if c in conds]
        print(f"LADDER judge {judge} | {case_id}: correct (P(truth)) "
              + " -> ".join(f"{c} {x['factors']['quality_wording']} {_rate(x['correct'])} "
                            f"({x['p_truth']})" for c, x in steps))
    print()


def auroc(correct: list[float], incorrect: list[float]) -> float | None:
    """The chance that a random correct decision carries a higher stated probability than
    a random incorrect one, ties counting half. 0.5 means the number carries no
    information; below 0.5, the judge is more confident when wrong. None when either
    class is empty."""
    if not correct or not incorrect:
        return None
    wins = sum((a > b) + 0.5 * (a == b) for a in correct for b in incorrect)
    return round(wins / (len(correct) * len(incorrect)), 3)


def _split(by_case: dict) -> tuple[list[float], list[float]]:
    """(stated probabilities when correct, when incorrect) over every case and repeat of
    one condition, given as {case_id: {run_index: (stated probability, correct)}}."""
    decisions = [d for runs in by_case.values() for d in runs.values()]
    return [s for s, ok in decisions if ok], [s for s, ok in decisions if not ok]


def _ranks(values: list[float]) -> list[float]:
    """Ranks from 1, tied values sharing the average of their ranks. Sorts once, so unlike
    `_midranks` it stays fast on the hundreds of decisions a shuffle test reranks."""
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start
        while end + 1 < len(order) and values[order[end + 1]] == values[order[start]]:
            end += 1
        for i in order[start:end + 1]:
            ranks[i] = (start + end) / 2 + 1
        start = end + 1
    return ranks


def auroc_p(by_case: dict, shuffles: int = SHUFFLES,
            seed: int = SHUFFLE_SEED) -> float | None:
    """One-sided p for AUROC above 0.5, with the case as the unit. `by_case` is one judge's
    condition: {case_id: {run_index: (stated probability, correct)}}.

    A case's repeats are near-copies -- temperature 0, and only the order of the options
    and reports changes -- so the judge answers them almost alike. A test that counted
    each decision as separate evidence would make p far too small. So whole cases are
    shuffled instead: each shuffle scores every case's stated probabilities against the
    right/wrong record of another case, repeat by repeat (a repeat has the same rotations
    in every case). p is the share of shuffles whose AUROC is at least the observed one,
    with the observed arrangement counted as one of them, so p is never 0. 1.0 when every
    value is tied, as when a judge states the same number on every answer. None when
    either class is empty."""
    cases = sorted(by_case)
    stated = [(case, run, s) for case in cases
              for run, (s, _) in sorted(by_case[case].items())]
    record = {(case, run): ok for case in cases for run, (_, ok) in by_case[case].items()}
    all_ranks = _ranks([s for _, _, s in stated])

    def shuffled_auroc(record_of: dict) -> float | None:
        """AUROC when each case's stated probabilities are scored against the record of
        case record_of[case]. A repeat missing from that record (a failed parse) is left
        out of this shuffle, and the rest are reranked."""
        labels = [record.get((record_of[case], run)) for case, run, _ in stated]
        keep = [i for i, label in enumerate(labels) if label is not None]
        ranks = (all_ranks if len(keep) == len(stated)
                 else _ranks([stated[i][2] for i in keep]))
        n_ok = sum(labels[i] for i in keep)
        n_bad = len(keep) - n_ok
        if not n_ok or not n_bad:
            return None
        rank_sum = sum(rank for rank, i in zip(ranks, keep) if labels[i])
        return (rank_sum - n_ok * (n_ok + 1) / 2) / (n_ok * n_bad)

    observed = shuffled_auroc({case: case for case in cases})
    if observed is None:
        return None
    rng = random.Random(seed)
    at_least = 0
    for _ in range(shuffles):
        donors = cases[:]
        rng.shuffle(donors)
        value = shuffled_auroc(dict(zip(cases, donors)))
        at_least += value is not None and value >= observed - 1e-9
    return (at_least + 1) / (shuffles + 1)


def discrimination_verdict(conds: dict) -> tuple[str, str]:
    """Discrimination check (proposal §5), from one judge's {condition: {case_id:
    {run_index: (stated probability, correct)}}}. A condition counts when both classes hold
    MIN_CLASS decisions; A0 never does, since with no report a right answer is a lucky
    guess about a made-up fact. The judge is retained when at least one counted condition
    has AUROC above 0.5 at one-sided p below SCREEN_ALPHA divided by the number counted,
    the p from `auroc_p`, which shuffles whole cases because a case's repeats are
    near-copies. At least one, not every: in X1 being wrong mostly means following the two
    agreeing reports, which a judge can do confidently -- the effect under study -- so
    AUROC can fall below 0.5 there although its numbers carry information. A judge
    stating the same number on every answer sits at 0.5 everywhere and fails. With no
    counted condition the check cannot be assessed, and the judge is EXCLUDED. This is the
    rule as first registered; since 2026-10-21 its verdict is printed but not applied
    (docs/decisions.md)."""
    counted = [c for c in sorted(conds, key=ORDER.index)
               if c != "A0" and min(map(len, _split(conds[c]))) >= MIN_CLASS]
    if not counted:
        return "EXCLUDED", (f"not assessable: no condition has {MIN_CLASS} correct and "
                            f"{MIN_CLASS} incorrect decisions")
    level = SCREEN_ALPHA / len(counted)
    p = {c: auroc_p(conds[c]) for c in counted}
    verdict = "retained" if min(p.values()) < level else "EXCLUDED"
    return verdict, (", ".join(f"{c} p {v:.4f}" for c, v in p.items())
                     + f"; passes below {SCREEN_ALPHA} / {len(counted)} = {level:.4f}")


def report_discrimination(records: list[dict]) -> None:
    """The proposal's second check (§5): does the stated probability of the chosen answer
    separate correct decisions from incorrect ones? Within condition, on the short arm,
    where every condition runs for every judge: pooled across conditions it would mostly
    measure the manipulation itself. The printed AUROC pools a condition's cases and
    repeats; its p-value treats the case as the unit (`auroc_p`). The class counts are
    printed alongside, since a handful of trials in one class makes the number
    meaningless. Reported for every judge, but it excludes none: in this study's
    conditions a wrong answer is almost always the two agreeing reports' claim, so AUROC
    there shows how sure a judge is when it follows them. The verdict of the rule as first
    registered is printed beside it, marked as not applied (docs/decisions.md,
    2026-10-21)."""
    groups = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for r in records:
        if r["arm"] == "short" and r.get("confidence_elicited") is not None:
            groups[r["judge_model"]][r["condition"]][r["case_id"]][r["run_index"]] = \
                (r["confidence_elicited"], bool(r["decision_correct"]))
    for judge, conds in sorted(groups.items()):
        parts = []
        for c in sorted(conds, key=ORDER.index):
            ok, bad = _split(conds[c])
            parts.append(f"{c} {_rate(auroc(ok, bad))} ({len(ok)}/{len(bad)})")
        print(f"DISCRIMINATION judge {judge}: AUROC (n correct/incorrect) " + ", ".join(parts))
        verdict, detail = discrimination_verdict(conds)
        print(f"  rule as first registered, not applied: {detail} -- would be "
              f"{verdict.lower()}")
    print()


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
    clipped. A clipped cell gives a bound, not a value, so every value computed from it
    reads "at ceiling"; a clipped A0 or A1 clips the unit, so then every value does
    (docs/decisions.md, 2026-10-21)."""
    need = ["A0", "A1", "A4", "A6", "A7"]
    if any(cells.get(c) is None or cells[c].get("p_truth") is None for c in need):
        return {"undefined": "missing P(truth) in " + str([c for c in need if not cells.get(c)])}
    p = {c: cells[c]["p_truth"] / 100 for c in need}
    clipped = {c for c, v in p.items() if not 0.01 <= v <= 0.99}
    l = {c: _logit(v) for c, v in p.items()}
    w = l["A1"] - l["A0"]
    if abs(w) < 0.2:
        return {"undefined": f"w = l(A1) - l(A0) = {w:.3f} < 0.2 logits",
                "clipped": len(clipped)}
    if w < 0:
        return {"undefined": f"anomaly: w = l(A1) - l(A0) = {w:.3f} is negative, one "
                             f"supporting report lowered belief in the truth",
                "anomaly": True, "clipped": len(clipped)}
    n = {c: round((l[c] - l["A0"]) / w, 2) for c in ("A4", "A6", "A7")}
    out = dict(n, w=round(w, 3), clipped=len(clipped), CN=round(n["A4"] - 1, 2),
               IS=round(n["A7"] - n["A4"], 2), RP=round(n["A4"] - n["A6"], 2))
    at = clipped | ({"A4", "A6", "A7"} if clipped & {"A0", "A1"} else set())
    uses = {"A4": {"A4"}, "A6": {"A6"}, "A7": {"A7"}, "CN": {"A4"}, "IS": {"A4", "A7"},
            "RP": {"A4", "A6"}, "w": {"A0", "A1"}}
    return {k: "at ceiling" if uses.get(k, set()) & at else v for k, v in out.items()}


def report_neff(records: list[dict], excluded: set = frozenset(),
                show_excluded: bool = False) -> None:
    """n_eff only for judges the confidence screen retains: a judge whose stated numbers
    do not order has no usable scale, so its n_eff is undefined even when the arithmetic
    would run. The undefined rate is itself reported per judge, and beside it how many
    cells have a value at ceiling. `show_excluded` prints that arithmetic for an excluded
    judge, marked as a check; the value still counts as undefined.

    Beside them, how many of the judge's agreement-block answers put 100 on one option: a
    judge that states 100 on whatever it picks has a mean P(truth) of 100 times its
    accuracy, which rises from P0 to P2, so ordering cannot catch it, and its n_eff would
    read its accuracy. A description, not a gate (docs/decisions.md, 2026-10-21)."""
    groups = defaultdict(lambda: defaultdict(list))
    at_100 = defaultdict(list)             # judge -> one bool per agreement-block answer
    for r in records:
        if r["arm"] == "short":
            groups[(r["judge_model"], r["case_id"])][r["condition"]].append(r)
            if r["condition"] in AGREEMENT_BLOCK and r.get("margin") is not None:
                at_100[r["judge_model"]].append(max(r["p"].values()) >= 100)
    undefined = defaultdict(list)          # judge -> one bool per case
    ceiling = defaultdict(list)            # judge -> one bool per case: a value at ceiling
    for (judge, case_id), conds in sorted(groups.items()):
        cells = {c: cell(rs) for c, rs in conds.items()}
        pt = {c: cells[c]["p_truth"] for c in ("A0", "A1", "A4", "A6", "A7") if c in cells}
        value = ({"undefined": "judge failed the confidence screen"} if judge in excluded
                 else neff(cells))
        if judge in excluded and show_excluded:
            value["for checking only, not a result"] = neff(cells)
        undefined[judge].append("undefined" in value)
        shown = value.get("for checking only, not a result", value)
        ceiling[judge].append("at ceiling" in shown.values())
        print(f"N_EFF judge {judge} | {case_id}: mean P(truth) {pt} -> {value}  "
              f"(normative A4 1, A6 1, A7 3)")
    for judge, flags in sorted(undefined.items()):
        print(f"N_EFF UNDEFINED judge {judge}: {sum(flags)}/{len(flags)} cells "
              f"({sum(flags) / len(flags):.2f}); a value at ceiling in "
              f"{sum(ceiling[judge])}/{len(flags)}; 100 stated on one option in "
              f"{_count(at_100[judge])} agreement-block answers")
    print()


def unbacked(r: dict, threshold: float = MARGIN_THRESHOLD) -> bool | None:
    """H6's flag on a forced-choice record: its stated numbers do not identify the answer
    given, because another option holds the highest probability (incoherent) or the top
    two are less than `threshold` points apart (near indifference; a tie at the top is a
    margin of 0). None when the record has no usable numbers."""
    if r.get("margin") is None:
        return None
    return r["coherent"] is False or r["margin"] < threshold


def _count(hits: list) -> str:
    return f"{sum(hits)}/{len(hits)} ({_rate(sum(hits) / len(hits) if hits else None)})"


def _mh_difference(strata: list[tuple[list, list]]) -> float | None:
    """Abstention rate in flagged trials minus in the rest, compared inside each stratum
    and then combined, a Mantel-Haenszel difference: each stratum is one condition, given
    as (abstained? for its flagged trials, for its other trials), and weighs
    n_flagged * n_other / n, so a condition with few of either kind counts for little.
    Strata missing either kind are left out; None when every one is."""
    weighted = weight = 0.0
    for flagged, other in strata:
        n1, n0 = len(flagged), len(other)
        if n1 and n0:
            weighted += (sum(flagged) * n0 - sum(other) * n1) / (n1 + n0)
            weight += n1 * n0 / (n1 + n0)
    return weighted / weight if weight else None


def h6_reading(conflict: list[bool], a7: list[bool], p0: list[bool]) -> str:
    """How one judge's H6 is read, with cut-offs fixed before the main run
    (docs/decisions.md, 2026-10-21). Each list holds one abstained? per abstention-arm
    trial: the conflict block's twins, A7 and P0. Abstaining in at least half of A7, where
    three independent sources agree, is abstaining everywhere; abstaining in under half of
    P0, where one irrelevant report settles nothing, is abstaining nowhere. Either is the
    README's nuisance case, so H6 is not testable for that judge."""
    half = lambda xs: bool(xs) and sum(xs) >= len(xs) / 2
    if half(a7):
        return ("not testable: abstained in at least half of its A7 trials, so it abstains "
                "everywhere")
    if any(conflict):
        return (f"the test applies: abstained in {sum(conflict)}/{len(conflict)} "
                f"conflict-block trials")
    if not p0:
        return "not assessed: no P0 trials"
    if half(p0):
        return ("clean null: abstained in at least half of its P0 trials, so it can, but "
                "never in the conflict block")
    return ("not testable: abstained in under half of its P0 trials, so it abstains "
            "nowhere")


def report_h6(records: list[dict], excluded: set = frozenset(),
              show_excluded: bool = False) -> None:
    """H6 (proposal §5), per judge. Observation, on the short arm's conflict block: how many
    records' stated numbers do not identify the answer given (`unbacked`). Test: does the
    judge abstain more in the same trials of the abstention arm -- same case, condition
    and repeat, so the same reports in the same order -- than in the trials whose numbers
    did identify the answer, read against its own abstention rate in A7?

    The two are compared inside each condition and then combined (`_mh_difference`),
    never across the block pooled. Close numbers and abstaining can both simply be
    commoner in some conditions than in others -- X1 leaves the conflict open, X5 settles
    it -- and pooling would turn that into an H6 effect that no single trial shows, the
    same reason discrimination stays within condition. Only for judges the confidence
    screen retains, since the flag reads stated numbers; `show_excluded` prints the
    others, marked as checks. The MARGIN_SENSITIVITY lines are declared in advance and are
    not the test.

    Beside A7, the abstention rate in P0 offered the abstain option, where one irrelevant
    report cannot settle the answer: a check added after the pilot, not the test. A7
    shows a judge that abstains everywhere; P0 shows one that abstains nowhere, even
    where the evidence is empty. Last, the reading those give, with fixed cut-offs
    (`h6_reading`; docs/decisions.md, 2026-10-21)."""
    forced, twins = defaultdict(dict), defaultdict(dict)
    a7, p0 = defaultdict(list), defaultdict(list)
    for r in records:
        key = (r["case_id"], r["condition"], r["run_index"])
        if r["arm"] == "short" and r["condition"] in CONFLICT_BLOCK:
            forced[r["judge_model"]][key] = r
        elif r["arm"] == "abstain" and r["parsing_status"] not in PARSE_FAILURES:
            if r["condition"] == "A7":
                a7[r["judge_model"]].append(r["abstained"])
            elif r["condition"] == "P0":
                p0[r["judge_model"]].append(r["abstained"])
            else:
                twins[r["judge_model"]][key] = r["abstained"]
    for judge, recs in sorted(forced.items()):
        label = ""
        if judge in excluded:
            if not show_excluded:
                print(f"H6 judge {judge}: not assessed, the judge failed the confidence "
                      "screen")
                continue
            label = " (failed the confidence screen: for checking only, not a result)"
        flags = [unbacked(r) for r in recs.values()]
        hit = sum(f is True for f in flags)
        inc = sum(r.get("coherent") is False for r in recs.values())
        print(f"H6 judge {judge}{label}: {hit}/{sum(f is not None for f in flags)} "
              f"conflict-block records do not identify the answer given ({inc} incoherent, "
              f"{hit - inc} by margin < {MARGIN_THRESHOLD})")

        def by_condition(threshold):
            """{condition: (abstained? in the twins of flagged trials, of the others)}"""
            pairs = defaultdict(lambda: ([], []))
            for key, r in recs.items():
                flag = unbacked(r, threshold)
                if key in twins[judge] and flag is not None:
                    pairs[key[1]][0 if flag else 1].append(twins[judge][key])
            return {c: pairs[c] for c in CONFLICT_BLOCK if c in pairs}

        def difference(threshold):
            d = _mh_difference(list(by_condition(threshold).values()))
            return "n/a" if d is None else f"{d:+.2f}"

        print("  abstained in the abstention arm, inside each condition:")
        for c, (flagged, other) in by_condition(MARGIN_THRESHOLD).items():
            print(f"    {c} flagged {_count(flagged)}, not flagged {_count(other)}")
        print(f"  flagged minus not flagged, inside conditions (Mantel-Haenszel): "
              f"{difference(MARGIN_THRESHOLD)}; own A7 {_count(a7[judge])}")
        if p0[judge]:
            print(f"  check beside A7, not the test: abstained in P0, one irrelevant report, "
                  f"{_count(p0[judge])}")
        print("  sensitivity, declared in advance, not the test: "
              + "; ".join(f"margin < {t}: {difference(t)}" for t in MARGIN_SENSITIVITY))
        conflict = [a for (_, c, _), a in twins[judge].items() if c in CONFLICT_BLOCK]
        print(f"  reading, cut-offs fixed before the main run: "
              f"{h6_reading(conflict, a7[judge], p0[judge])}")
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


def _midranks(v: list) -> list[float]:
    return [sum((y < x) + 0.5 * (y == x) for y in v) + 0.5 for x in v]


def page_test(by_case: dict) -> tuple:
    """Page's test for ordered alternatives, the cases as blocks: L sums, over cases, the
    rank of each level's P(truth) times its predicted rank (P0 1, P1 2, P2 3). The p-value
    is exact and one-sided: with no ordering, each case's ranks are equally likely in any
    of their 6 orders, ties kept as midranks. rho, L rescaled to [-1, 1], is the matching
    rank correlation: the mean Spearman correlation between predicted and observed order,
    exactly so when no case has ties. Cases missing a level are left out.
    Returns (L, rho, p, cases used)."""
    rows = [_midranks(v) for v in by_case.values() if None not in v]
    if not rows:
        return None, None, None, 0
    page = lambda r: sum(w * x for w, x in zip((1, 2, 3), r))
    null = Counter({0: 1})              # L summed over the cases so far -> ways to get it
    for r in rows:
        step = Counter(page(order) for order in permutations(r))
        nxt = Counter()
        for a, m in null.items():
            for b, k in step.items():
                nxt[a + b] += m * k
        null = nxt
    L = sum(page(r) for r in rows)
    p = sum(m for s, m in null.items() if s >= L) / 6 ** len(rows)
    return L, round(L / (2 * len(rows)) - 6, 3), p, len(rows)


def screen_verdict(by_case: dict) -> tuple[str, str]:
    """Ordering check (proposal §5): stated P(truth), per case the mean over the option
    rotations, should rise P0 < P1 < P2 on the judge's own scale; absolute values are not
    scored. Assessed across cases by a rank correlation and Page's test, not by
    inspection: the judge is EXCLUDED from probability-based analyses unless the one-sided
    p is below SCREEN_ALPHA. Per-case values are always shown."""
    L, rho, p, n = page_test(by_case)
    verdict = "retained" if p is not None and p < SCREEN_ALPHA else "EXCLUDED"
    detail = "; ".join(f"{cid} {', '.join(str(x) for x in v)}" for cid, v in sorted(by_case.items()))
    if n:
        detail += f" -- Page's L {L}, rank correlation {rho}, one-sided p {p:.4f}, {n} cases"
    if 6 ** -n >= SCREEN_ALPHA:         # even perfect order in every case could not pass
        detail += f" (too few cases to reach p < {SCREEN_ALPHA})"
    return verdict, detail


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
