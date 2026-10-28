"""
The confidence cross-check, read after the run (docs/decisions.md, 2026-10-26): for each
auxiliary model, its stated P(truth) beside the token probability of the truth's option
number at the answer's digit. Both are read the way the screen reads stated numbers, per
case the mean over the four rotations at P0, P1 and P2, with the scorer's Page's test, and
then against each other trial by trial. It describes; no test was fixed for it. No API
calls.

    uv run python -m tools.crosscheck runs/main/trials-cross-check.jsonl \
        runs/main/trials-cross-check-m12.jsonl

A token probability is the four numbers' share of the top alternatives the provider
returned at that position (five per token), normalised over the four. M10 is left out:
its options, 2 to 5 passes, can be read as option numbers, and M12 takes its place
(docs/decisions.md, 2026-10-28).
"""

import math
import sys
from collections import defaultdict

from pipeline.score import load, page_test

NUMBERS = {"1", "2", "3", "4"}
LEFT_OUT = {"M10"}      # an answer of 3 may mean option 3 or 3 passes


def _mean(xs) -> float:
    return sum(xs) / len(xs)


def answer_position(tokens: list[dict]) -> int | None:
    """The token that holds the answer's number: the first number after '"answer"'."""
    text = ""
    for i, t in enumerate(tokens):
        if '"answer"' in text and t["token"].strip() in NUMBERS:
            return i
        text += t["token"]
    return None


def number_probabilities(token: dict) -> tuple[dict, float]:
    """Probability per option number among the token's top alternatives, and the share
    of the probability mass the four numbers hold."""
    d = defaultdict(float)
    for alt in token["top_logprobs"]:
        if alt["token"].strip() in NUMBERS:
            d[alt["token"].strip()] += math.exp(alt["logprob"])
    return d, sum(d.values())


def _midranks(v: list) -> list[float]:
    return [sum((y < x) + 0.5 * (y == x) for y in v) + 0.5 for x in v]


def spearman(a: list, b: list) -> float:
    ra, rb = _midranks(a), _midranks(b)
    ma, mb = _mean(ra), _mean(rb)
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    return cov / math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))


def crosscheck(records: list[dict]) -> None:
    for judge in sorted({r["judge_model"] for r in records}):
        stated = defaultdict(lambda: defaultdict(list))   # case -> level -> P(truth)
        token = defaultdict(lambda: defaultdict(list))
        pairs, share, agree, p0_stated, p0_token = [], [], 0, [], []
        by_level = defaultdict(list)
        rs = [r for r in records if r["judge_model"] == judge]
        for r in rs:
            i = answer_position(r.get("token_logprobs") or [])
            if r.get("p_truth") is None or i is None:
                continue
            d, s = number_probabilities(r["token_logprobs"][i])
            # options are numbered in the order shown (pipeline/prompt.py)
            truth = str(r["answer_options"].index(r["world_truth"]) + 1)
            tp = 100 * d.get(truth, 0.0) / s
            stated[r["case_id"]][r["condition"]].append(r["p_truth"])
            token[r["case_id"]][r["condition"]].append(tp)
            pairs.append((r["p_truth"], tp))
            by_level[r["condition"]].append((r["p_truth"], tp))
            share.append(s)
            agree += max(d, key=d.get) == r["token_logprobs"][i]["token"].strip()
            if r["condition"] == "P0":
                p0_stated.append(max(r["p"].values()))
                p0_token.append(100 * max(d.values()) / s)
        print(f"== judge {judge}: {len(pairs)} of {len(rs)} trials with a stated P(truth) "
              f"and an answer number")
        for name, src in (("stated", stated), ("token", token)):
            by_case = {c: [round(_mean(v[k]), 1) if v.get(k) else None
                           for k in ("P0", "P1", "P2")] for c, v in src.items()}
            L, rho, p, n = page_test(by_case)
            levels = [_mean([v[j] for v in by_case.values() if v[j] is not None])
                      for j in range(3)]
            print(f"{name} P(truth), mean over cases at P0, P1, P2: "
                  + ", ".join(f"{x:.1f}" for x in levels)
                  + f"; Page's L {L}, rank correlation {rho}, one-sided p {p:.4f}, {n} cases")
        s, t = zip(*pairs)
        print(f"stated against token P(truth), trial by trial: Spearman {spearman(s, t):.2f}, "
              f"mean absolute difference {_mean([abs(a - b) for a, b in pairs]):.1f} points")
        # within one level, so the gap between levels does not carry the correlation; a
        # level where either number never changes has none
        within = []
        for k in ("P0", "P1", "P2"):
            a, b = zip(*by_level[k])
            within.append(f"{spearman(a, b):.2f}" if min(len(set(a)), len(set(b))) > 1
                          else "none (no spread)")
        print("the same within P0, P1, P2: Spearman " + ", ".join(within))
        print(f"P0, the irrelevant report: the largest stated p is {_mean(p0_stated):.1f} on "
              f"average, the largest token probability {_mean(p0_token):.1f}")
        print(f"the four numbers hold {_mean(share):.3f} of the top alternatives' mass on "
              f"average; the answer is the most likely number in {agree}/{len(pairs)}")
        print()


if __name__ == "__main__":
    print(f"left out: {', '.join(sorted(LEFT_OUT))} (docs/decisions.md, 2026-10-28)\n")
    crosscheck([r for path in sys.argv[1:] for r in load(path)
                if r["case_id"] not in LEFT_OUT])
