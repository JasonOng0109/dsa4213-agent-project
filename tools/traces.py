"""
The reasoning comparison's trace reading (docs/decisions.md, 2026-10-28): each trace's
code, joined to its trial through the key, crossed with the decision per condition and
length, over all 24 trials of each cell, with *none* as its own row. Run only once the
codes are committed. No API calls.

    uv run python -m tools.traces runs/main/traces runs/main/trials-reasoning-on.jsonl

The folder holds key.json (random id -> trial id), codes-settled.json and each coder's
codes (random id -> {"code", "quote"}). A trial with no thinking text codes as *none*.
"""

import json
import os
import sys
from collections import Counter

from pipeline.score import load

CODES = ("none", "noticed", "not noticed")


def reading(trials: list[dict], code_of: dict[str, str]) -> None:
    """Per condition and length: trials under each code, and how many chose the
    independent report, the only report that states the truth in X1, X3 and X5."""
    print(f"{'cell':<10}" + "".join(f"{c + ' (chose it)':>24}" for c in CODES) + f"{'trials':>8}")
    cells = sorted({(t["condition"], t["length"]) for t in trials})
    for cond, length in cells:
        ts = [t for t in trials if (t["condition"], t["length"]) == (cond, length)]
        n = Counter(code_of.get(t["trial_id"], "none") for t in ts)
        chose = Counter(code_of.get(t["trial_id"], "none") for t in ts if t["decision_correct"])
        print(f"{cond + ' ' + length:<10}"
              + "".join(f"{f'{n[c]} ({chose[c]})':>24}" for c in CODES) + f"{len(ts):>8}")


def main(folder: str, log: str) -> None:
    with open(os.path.join(folder, "key.json")) as f:
        key = json.load(f)
    trials = load(log)
    has_text = {t["trial_id"] for t in trials if (t.get("reasoning_text") or "").strip()}
    assert set(key.values()) == has_text, "the key must cover exactly the traces with text"
    codes = {}
    for name in ("settled", "coder1", "coder2"):
        with open(os.path.join(folder, f"codes-{name}.json")) as f:
            codes[name] = {key[i]: v["code"] if isinstance(v, dict) else v
                           for i, v in json.load(f).items()}
    agree = sum(codes["coder1"][t] == codes["coder2"][t] for t in key.values())
    print(f"the coders agreed on {agree} of {len(key)} traces with text\n")
    print("== settled codes")
    reading(trials, codes["settled"])
    if agree < len(key):
        for name in ("coder1", "coder2"):
            print(f"\n== {name}'s codes")
            reading(trials, codes[name])


if __name__ == "__main__":
    main(*sys.argv[1:3])
