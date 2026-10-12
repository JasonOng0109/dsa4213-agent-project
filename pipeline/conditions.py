"""
The condition builder (proposal §4): the thirteen conditions of one case, built from
its frozen reports, plus the three rungs of the graded wording ladder and the three
levels of the confidence screen.

A0-A7 form the agreement block, X1-X5 the conflict block, and W1-W3 are X5 with its
quality statement softened (proposal §4.1). Every trial carries its
condition's factor vector, so the scorer groups by factor rather than by name. Options,
the independent report's slot and (long reports) the operative sentence's position come
from rotation_schedule(), never from shuffling, so each position is covered a known
number of times.

The shared source is always B, the strong one (R14): the agreement block repeats
evidence that supports the truth, and A appears only in X1-X5.
"""

from __future__ import annotations
import random

AGENT_LABELS = ["Agent A", "Agent B", "Agent C"]
SHARED_SOURCE = "B"
CUE_POSITIONS = ["start", "middle", "end"]
LONG_WORDS = (88, 96)      # every long report is inside this band ...
LONG_MATCH = 1.10          # ... and the longest is at most this times the shortest.
                           # The two agree: 96 / 88 = 1.091 (proposal §4.1)

_F = ("reports", "messages", "agents", "sources", "conflict",
      "provenance_shown", "dependence_stated", "quality_stated", "quality_wording")
FACTORS = {cond: dict(zip(_F, vals)) for cond, vals in {
    "A0": (0, 0, 0, 0, "no", "none", False, False, None),
    "A1": (1, 1, 1, 1, "no", "none", False, False, None),
    "A2": (3, 1, 1, 1, "no", "none", False, False, None),
    "A3": (3, 3, 1, 1, "no", "none", False, False, None),
    "A4": (3, 3, 3, 1, "no", "none", False, False, None),
    "A5": (3, 3, 3, 1, "no", "opaque ID", False, False, None),
    "A6": (3, 3, 3, 1, "no", "opaque ID", True, False, None),
    "A7": (3, 3, 3, 3, "no", "none", False, False, None),
    "X1": (3, 3, 3, 2, "2-vs-1", "none", False, False, None),
    "X2": (3, 3, 3, 2, "2-vs-1", "named type", False, False, None),
    "X3": (3, 3, 3, 2, "2-vs-1", "none", True, False, None),
    "X4": (3, 3, 3, 2, "2-vs-1", "none", False, True, "categorical"),
    "X5": (3, 3, 3, 2, "2-vs-1", "none", True, True, "categorical"),
    # the graded wording ladder: X5 with only the intensity of the quality statement varied,
    # so X5's categorical wording is the ceiling of a dose-response curve
    "W1": (3, 3, 3, 2, "2-vs-1", "none", True, True, "somewhat"),
    "W2": (3, 3, 3, 2, "2-vs-1", "none", True, True, "considerably"),
    "W3": (3, 3, 3, 2, "2-vs-1", "none", True, True, "far"),
}.items()}
AGREEMENT_BLOCK = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]
CONFLICT_BLOCK = ["X1", "X2", "X3", "X4", "X5"]
LADDER = ["W1", "W2", "W3"]
ABSTAIN_ARM = CONFLICT_BLOCK + ["A7"]   # A7: the judge's own no-conflict baseline

# Screen levels: one report each, no provenance, no note. The shared factors are A1's
# (one report, one source); `informativeness` is what the screen varies.
SCREEN_LEVELS = {"P0": "irrelevant", "P1": "partial", "P2": "determinate"}
SCREEN_FACTORS = {lvl: dict(FACTORS["A1"], informativeness=inf)
                  for lvl, inf in SCREEN_LEVELS.items()}


def rotation_schedule(run_index: int) -> dict:
    """The rotations for repeat `run_index` (1-based).
    - indep_slot (period 3) and option_rotation, the truth's position (period 4), are
      coprime: 12 repeats cover all 12 pairs once.
    - wrong_offset (period 3) places A's claim among the three positions left after the
      truth, so truth and wrong claim are not always adjacent. In the conflict block it
      is (r-1) + (r-1)//4, mod 3: every (truth, offset) pair once in 12 repeats, and NOT
      in lockstep with indep_slot, which (r-1) mod 3 would be. The agreement block has
      no independent slot to confound, so it uses (r-1) mod 3, even over its 6 repeats.
      The two agree for r = 1-4.
    - cue_position is offset by (r-1)//3 so it does not move in lockstep with the slot
      either: 9 repeats cover all 9 slot x cue pairs."""
    i = run_index - 1
    slot = i % 3
    return {"indep_slot": slot,
            "option_rotation": i % 4,
            "wrong_offset": (i + i // 4) % 3,
            "wrong_offset_agreement": i % 3,
            "cue_position": CUE_POSITIONS[(slot + i // 3) % 3]}


def base_options(case: dict) -> list[str]:
    """The unordered option set: the truth, A's claim, then the distractors."""
    return [case["world_truth"], case["sources"]["A"]["claim"]] + list(case.get("distractors", []))


def rotated_options(case: dict, option_rotation: int, wrong_offset: int = 0) -> list[str]:
    """Truth at index option_rotation % k; A's claim at position wrong_offset among the
    remaining ones; distractors fill the rest in authored order."""
    truth, wrong, *distractors = base_options(case)
    k = 2 + len(distractors)
    t = option_rotation % k
    rest = [i for i in range(k) if i != t]
    w = rest.pop(wrong_offset % len(rest))
    opts = [None] * k
    opts[t], opts[w] = truth, wrong
    for i, d in zip(rest, distractors):
        opts[i] = d
    return opts


def embed_in_filler(filler: list[str], sentence: str, cue_position: str) -> str:
    """Long report: the operative sentence before, in the middle of, or after the slot's
    filler sentences."""
    cut = {"start": 0, "middle": len(filler) // 2, "end": len(filler)}[cue_position]
    return " ".join(filler[:cut] + [sentence] + filler[cut:])


def check_long_lengths(case_id: str, reports: list[dict]) -> None:
    """Fail loudly rather than emit a long report off target, so length cannot
    substitute for provenance. The fix is in the paraphrase or the filler, never here."""
    n = [len(r["text"].split()) for r in reports]
    if not n:
        return
    lo, hi = LONG_WORDS
    words = [(r["source_key"], r["slot"], w) for r, w in zip(reports, n)]
    if not all(lo <= w <= hi for w in n) or max(n) > LONG_MATCH * min(n):
        raise ValueError(f"{case_id}: long reports off target ({lo}-{hi} words each, "
                         f"longest/shortest <= {LONG_MATCH}): got {max(n)}/{min(n)}; "
                         f"(source, slot, words) = {words}")


def _reports_for(frozen_case: dict, source_key: str, k: int) -> list[dict]:
    """The first k accepted reports of a source."""
    accepted = frozen_case[source_key]["accepted"]
    if len(accepted) < k:
        raise ValueError(f"Source {source_key} has only {len(accepted)} accepted "
                         f"reports, need {k}. Re-run generation.")
    return [{"source_key": source_key, "text": accepted[i]["text"]} for i in range(k)]


def _shuffled(reports: list[dict], rng: random.Random) -> list[dict]:
    order = reports[:]
    rng.shuffle(order)
    return order


def build_conditions(case_id: str, case: dict, frozen_case: dict, rng: random.Random,
                     indep_slot: int = 0, option_rotation: int = 0, wrong_offset: int = 0,
                     wrong_offset_agreement: int | None = None, allow_abstain: bool = False,
                     length: str = "short", cue_position: str | None = None) -> list[dict]:
    """All sixteen trials of one case (thirteen conditions and three ladder rungs) at one
    point in the rotation schedule."""
    if length == "long" and cue_position not in CUE_POSITIONS:
        raise ValueError(f"long reports need a cue_position in {CUE_POSITIONS}")
    if wrong_offset_agreement is None:
        wrong_offset_agreement = wrong_offset

    def place(reps, labels, prov_ids=None):
        """Report i goes in slot i and gets filler set i -- by SLOT, never by source
        (R12), so two reports of one source never share padding."""
        out = []
        for i, r in enumerate(reps):
            text = r["text"]
            if length == "long":
                text = embed_in_filler(case["filler_sets"][i], text, cue_position)
            out.append({"source_key": r["source_key"], "paraphrase": r["text"],
                        "text": text, "slot": i,
                        "filler_set": i if length == "long" else None,
                        "agent_label": labels[i],
                        "provenance_id": prov_ids[i] if prov_ids else None})
        if length == "long":
            check_long_lengths(case_id, out)
        return out

    def trial(cond, reports, note=None, majority=None):
        # each block takes its own wrong-claim offset (see rotation_schedule); the ladder
        # rungs are conflict trials
        conflict = cond in CONFLICT_BLOCK or cond in LADDER
        off = wrong_offset if conflict else wrong_offset_agreement
        return _trial(case_id, cond, case, rotated_options(case, option_rotation, off),
                      reports, note, majority, option_rotation, off, allow_abstain,
                      length, cue_position, indep_slot if conflict else None)

    shared_claim = case["sources"][SHARED_SOURCE]["claim"]
    trials = [trial("A0", [])]
    trials.append(trial("A1", place(_reports_for(frozen_case, SHARED_SOURCE, 1), AGENT_LABELS)))

    order = _shuffled(_reports_for(frozen_case, SHARED_SOURCE, 3), rng)
    a4 = place(order, AGENT_LABELS)
    # A2: A4's three texts as ONE message, joined with a single space -- a blank line or
    # connective would reintroduce the segmentation A2 exists to remove. Exempt from the
    # length check by construction.
    trials.append(trial("A2", [{
        "source_key": SHARED_SOURCE, "paraphrase": " ".join(r["paraphrase"] for r in a4),
        "text": " ".join(r["text"] for r in a4), "slot": 0,
        "filler_set": [r["filler_set"] for r in a4] if length == "long" else None,
        "agent_label": "Agent A", "provenance_id": None}], majority=shared_claim))
    trials.append(trial("A3", [dict(r, agent_label=f"Agent A, report {i+1}")
                               for i, r in enumerate(a4)], majority=shared_claim))
    trials.append(trial("A4", a4, majority=shared_claim))
    a5 = [dict(r, provenance_id="S-001") for r in a4]
    trials.append(trial("A5", a5, majority=shared_claim))
    trials.append(trial("A6", a5, majority=shared_claim, note=(
        f"Note: {AGENT_LABELS[0]}, {AGENT_LABELS[1]}, and {AGENT_LABELS[2]} all "
        f"obtained their information from the same underlying source (S-001).")))
    indep = [_reports_for(frozen_case, k, 1)[0] for k in "BCD"]
    trials.append(trial("A7", place(_shuffled(indep, rng), AGENT_LABELS)))

    # conflict block: two reports of weak A, one of strong B at indep_slot
    order_x = _shuffled(_reports_for(frozen_case, "A", 2), rng)
    order_x.insert(indep_slot % 3, _reports_for(frozen_case, "B", 1)[0])
    x1 = place(order_x, AGENT_LABELS)
    pair = [r for r in x1 if r["source_key"] == "A"]
    assert pair[0]["slot"] != pair[1]["slot"], "shared-source reports must not share filler"
    weak_claim = case["sources"]["A"]["claim"]
    c0, c1 = (r["agent_label"] for r in pair)
    ind = next(r["agent_label"] for r in x1 if r["source_key"] == "B")
    # X3 names agents, not sources, so it needs no identifier
    dep = (f"Note: {c0} and {c1} obtained their information from the same underlying "
           f"source; {ind}'s information comes from a different, independent source.")
    # X4 states quality without implying anything about dependence, in number-neutral
    # wording; X5 adds the quality statement to X3's note
    qual5 = (f" {ind}'s source is a primary, authoritative record; the source shared "
             f"by {c0} and {c1} is a secondhand or unofficial one.")
    qual4 = (f"Note: {ind}'s source is a primary, authoritative record; the other "
             f"reports rest on secondhand or unofficial material.")
    x2 = [dict(r, provenance_id=case["sources"][r["source_key"]]["provenance"]["type"])
          for r in x1]
    trials.append(trial("X1", x1, majority=weak_claim))
    trials.append(trial("X2", x2, majority=weak_claim))
    trials.append(trial("X3", x1, note=dep, majority=weak_claim))
    trials.append(trial("X4", x1, note=qual4, majority=weak_claim))
    trials.append(trial("X5", x1, note=dep + qual5, majority=weak_claim))
    for w in LADDER:
        rung = (f" {ind}'s source is {FACTORS[w]['quality_wording']} more reliable than "
                f"the source shared by {c0} and {c1}.")
        trials.append(trial(w, x1, note=dep + rung, majority=weak_claim))
    return trials


def build_repeat(case_id: str, case: dict, frozen_case: dict, run_index: int,
                 seed: int = 42, length: str = "short",
                 allow_abstain: bool = False) -> list[dict]:
    """All sixteen trials for repeat `run_index` (1-based), with that repeat's
    rotations. The rng depends on the repeat only, so every arm of one repeat shows the
    same reports in the same order."""
    s = rotation_schedule(run_index)
    return build_conditions(case_id, case, frozen_case, random.Random(seed + run_index - 1),
                            indep_slot=s["indep_slot"], option_rotation=s["option_rotation"],
                            wrong_offset=s["wrong_offset"],
                            wrong_offset_agreement=s["wrong_offset_agreement"],
                            allow_abstain=allow_abstain, length=length,
                            cue_position=s["cue_position"] if length == "long" else None)


def build_screen(case_id: str, case: dict, frozen_case: dict,
                 option_rotation: int = 0, wrong_offset: int = 0) -> list[dict]:
    """The confidence screen: three single-report trials graded by informativeness, not
    by evidence count. P0 is a filler sentence (non-decisive by R9), P1 the authored
    `screen_partial`, P2 B's first frozen report. No provenance, no note, short only."""
    opts = rotated_options(case, option_rotation, wrong_offset)
    texts = {"P0": ("filler", case["filler_sets"][0][0]),
             "P1": ("screen_partial", case["screen_partial"]),
             "P2": ("B", _reports_for(frozen_case, "B", 1)[0]["text"])}
    trials = []
    for lvl, (src, text) in texts.items():
        rep = {"source_key": src, "paraphrase": text, "text": text, "slot": 0,
               "filler_set": None, "agent_label": "Agent A", "provenance_id": None}
        t = _trial(case_id, lvl, case, opts, [rep], None, None, option_rotation,
                   wrong_offset, False, "short", None, None)
        t.update(factors=SCREEN_FACTORS[lvl], arm="screen")
        trials.append(t)
    return trials


def _trial(case_id, condition, case, opts, reports, provenance_note, majority_claim,
           option_rotation, wrong_offset, allow_abstain, length, cue_position, indep_slot):
    return {
        "case_id": case_id,
        "condition": condition,
        "arm": "ladder" if condition in LADDER else "abstain" if allow_abstain else length,
        "factors": FACTORS.get(condition),
        "domain": case["domain"],
        "question": case["question"],
        "answer_options": opts,
        "allow_abstain": allow_abstain,
        "world_truth": case["world_truth"],
        "majority_claim": majority_claim,
        "quality_dimension": case["quality_dimension"],
        "difficulty_tier": case.get("difficulty_tier"),
        "length": length,
        "cue_position": cue_position if length == "long" else None,
        "option_rotation": option_rotation,
        "wrong_offset": wrong_offset,
        "indep_slot": indep_slot,
        "reports": reports,
        "provenance_note": provenance_note,
        "presentation_order_realized": [r["agent_label"] + "<-" + r["source_key"]
                                        for r in reports],
    }
