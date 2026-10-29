"""
Decision stability over cases (README, "Measures, in order of weight", measure 2). The
scorer prints each cell's stability beside its chance baseline; this sums the cells up per
judge, arm and condition: the mean stability over cases, how many cells had every repeat
give the same answer, and the chance baseline at that repeat count. It reads the same
trial logs and reuses the scorer's cells, so its numbers match the scorer's tables. No API
calls.

    uv run python -m tools.stability runs/main/trials-*.jsonl
"""

import sys
from collections import defaultdict

from pipeline.conditions import AGREEMENT_BLOCK, CONFLICT_BLOCK
from pipeline.score import ORDER, cell, load


def summary(label: str, cells: list[dict]) -> str:
    cells = [c for c in cells if c["stability"] is not None]
    stab = [c["stability"] for c in cells]
    values = lambda key, fmt: "/".join(fmt.format(v) for v in sorted({c[key] for c in cells}))
    return (f"{label}: mean {sum(stab) / len(stab):.2f} over {len(stab)} cells, every repeat "
            f"agrees in {sum(s == 1.0 for s in stab)}/{len(stab)}; repeats "
            f"{values('n_stability', '{}')}, chance {values('stability_chance', '{:.2f}')}")


def report(records: list[dict]) -> None:
    by = defaultdict(lambda: defaultdict(list))   # (judge, arm) -> (case, condition) -> trials
    for r in records:
        by[(r["judge_model"], r["arm"])][(r["case_id"], r["condition"])].append(r)
    for (judge, arm), groups in sorted(by.items()):
        cells = {key: cell(rs) for key, rs in groups.items()}
        conds = sorted({k for _, k in cells}, key=ORDER.index)
        print(f"== judge {judge} | arm {arm}")
        for k in conds:
            print("  " + summary(k, [c for (_, kk), c in cells.items() if kk == k]))
        # A0 shows no reports, so the agreement block's pooled line leaves it out
        for name, block in (("A1-A7", AGREEMENT_BLOCK[1:]), ("X1-X5", CONFLICT_BLOCK)):
            if set(block) <= set(conds):
                print("  " + summary(name, [c for (_, k), c in cells.items() if k in block]))
        print()


if __name__ == "__main__":
    report([r for path in sys.argv[1:] for r in load(path)])
