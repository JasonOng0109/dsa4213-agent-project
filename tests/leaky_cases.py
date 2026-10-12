"""
Deliberately broken cases: the linter's test fixture.

Every case is a copy of one clean base case with exactly one planted fault,
so a flag can only come from the plant. EXPECTED lists the rules each case
must be flagged for -- usually one; a few plants unavoidably break a second
rule too, and say so. SPEC_ASYMMETRY carries a specificity asymmetry, which
docs/authoring-rules.md says no script can see: the linter must pass it, and a
human reviewer must not. SCREEN_NAMES_OPTIONS has a screen statement that
names two options outright; screen statements are not sources (R15), so R8
and R9 must not fire on it.

    python -m pipeline.lint tests.leaky_cases   # must exit non-zero
    pytest tests/test_lint.py                   # checks the exact flags

The base case is self-contained rather than derived from M1, so rewriting M1
cannot silently change what this fixture tests.
"""

import copy

_BASE = {
    "case_id": "FX",
    "domain": "product_spec",
    "question": "How long does a full recharge of the Veltro K7 power bank take?",
    "world_truth": "4 hours",
    "distractors": ["3 hours", "8 hours"],
    "quality_dimension": "method",
    "difficulty_tier": "T2",
    # screen level P1: true, keeps the truth, rules out 6 and 8 hours
    "screen_partial": "The Veltro K7 power bank goes from empty to full in under five hours.",
    "filler_sets": [
        ["The Veltro K7 has two USB-C ports and one USB-A port.",
         "Its casing is aluminium with a matte finish."],
        ["The Veltro K7 weighs about as much as a paperback book.",
         "A braided cable ships in the box."],
        ["The Veltro K7 is sold in grey and dark blue.",
         "Four small lights on the side show the charge level."],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "6 hours",
            "provenance": {"type": "forum post by an owner", "authority": "individual",
                           "quality": "weak", "why": "one owner's rough estimate"},
            "content": "Charging a Veltro K7 power bank from empty to full needs 6 hours.",
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "4 hours",
            "provenance": {"type": "Veltro K7 technical datasheet", "authority": "institutional",
                           "quality": "strong", "why": "manufacturer's measured specification"},
            "content": "The Veltro K7 power bank requires 4 hours to go from empty to full.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "4 hours",
            "provenance": {"type": "independent test lab report", "authority": "institutional",
                           "quality": "strong", "why": "measured under controlled conditions"},
            "content": "Veltro K7 power bank, empty to full: 4 hours.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "4 hours",
            "provenance": {"type": "Veltro K7 user manual", "authority": "institutional",
                           "quality": "strong", "why": "shipped by the manufacturer"},
            "content": "A Veltro K7 power bank goes from empty to full in 4 hours.",
            "n_paraphrases_needed": 1,
        },
    },
}


def _variant(cid, edit):
    case = copy.deepcopy(_BASE)
    case["case_id"] = cid
    edit(case)
    return case


def _set(path, value):
    """Edit that sets case[path[0]][path[1]]... = value."""
    def edit(case):
        d = case
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = value
    return edit


_PLANTS = [
    # (case id, rules it must be flagged for, edit)
    ("F01_authored_options", {"R5"},
     _set(["answer_options"], ["4 hours", "6 hours", "3 hours", "8 hours"])),
    ("F02_one_distractor", {"R8"},
     _set(["distractors"], ["3 hours"])),
    # a distractor equal to A's claim is necessarily also named in A's claim/content
    ("F03_distractor_is_claim", {"R8", "R8b"},
     _set(["distractors"], ["3 hours", "6 hours"])),
    ("F04_two_wrong_sources", {"one-wrong"},
     lambda c: c["sources"]["C"].update(
         claim="6 hours", content="Veltro K7 power bank, empty to full: 6 hours.")),
    ("F05_distractor_in_provenance", {"R8b"},
     _set(["sources", "B", "provenance", "why"],
          "manufacturer's specification; the 3 hours figure belongs to the K5")),
    ("F06_distractor_in_filler", {"R9"},
     lambda c: c["filler_sets"][1].append("A 3 hours top-up is common for owners.")),
    ("F07_truth_in_filler", {"R9"},
     lambda c: c["filler_sets"][2].append("Most owners leave it plugged in for 4 hours.")),
    ("F08_supersession_in_A", {"R1"},
     _set(["sources", "A", "content"],
          "Charging a Veltro K7 power bank from empty to full now needs 6 hours.")),
    ("F09_hearsay_in_A", {"R2"},
     _set(["sources", "A", "content"],
          "Apparently, charging a Veltro K7 power bank from empty to full needs 6 hours.")),
    ("F10_attribution_in_B", {"R2"},
     _set(["sources", "B", "content"],
          "According to Veltro, the K7 power bank requires 4 hours to go from empty to full.")),
    ("F11_staleness_in_filler", {"R3"},
     lambda c: c["filler_sets"][0].append("Older units had a glossy finish.")),
    ("F12_date_in_D", {"R3"},
     _set(["sources", "D", "content"],
          "Since March 2025 a Veltro K7 power bank goes from empty to full in 4 hours.")),
    ("F13_doc_type_in_filler", {"R10"},
     lambda c: c["filler_sets"][0].append("This table lists every port on the Veltro K7.")),
    ("F14_register_in_filler", {"R10"},
     lambda c: c["filler_sets"][1].append("You can charge a phone twice from it.")),
    ("F15_two_sentence_content", {"R11"},
     _set(["sources", "B", "content"],
          "The Veltro K7 power bank requires 4 hours to go from empty to full. "
          "It charges over USB-C.")),
    ("F16_filler_per_source", {"R12"},
     _set(["sources", "A", "filler"], ["Its casing is aluminium with a matte finish."])),
    ("F17_two_filler_sets", {"R12"},
     lambda c: c["filler_sets"].pop()),
    ("F18_shared_filler_sentence", {"R12"},
     lambda c: c["filler_sets"][2].append(c["filler_sets"][0][1])),
    ("F19_question_echoes_B", {"R13"},
     _set(["question"],
          "How long does the Veltro K7 power bank require to recharge fully?")),
    ("F20_provenance_missing_type", {"R2"},
     lambda c: c["sources"]["B"]["provenance"].pop("type")),
    ("F21_shared_source_field", {"R14"},
     _set(["official_shared_source"], "B")),
    ("F22_A_three_paraphrases", {"R14"},
     _set(["sources", "A", "n_paraphrases_needed"], 3)),
    ("F23_no_screen_partial", {"R15"},
     lambda c: c.pop("screen_partial")),
    ("F24_screen_time_marker", {"R3"},
     _set(["screen_partial"],
          "The latest Veltro K7 power bank goes from empty to full in under five hours.")),
    ("F26_D_copies_B_frame", {"R17"},
     _set(["sources", "D", "content"],
          "The Veltro K7 power bank needs 4 hours to go from empty to full.")),
    # Must NOT be flagged: C echoes the question's verb, but C
    # never stands opposite a conflicting report, so nothing can point at a
    # winner. Printed as an R13 note only.
    ("F27_question_verb_in_C", set(),
     _set(["sources", "C", "content"],
          "Veltro K7 power bank: a recharge from empty to full takes 4 hours.")),
    ("F25_screen_two_sentences", {"R11"},
     _set(["screen_partial"],
          "The Veltro K7 power bank goes from empty to full quickly. It needs under five hours.")),
]

# Not flaggable, and must not be flagged: B names a narrower scope (the
# bundled charger) than A's general statement, so B dominates as an exception
# to A's rule whatever the provenance says. Only a human reviewer catches this.
SPEC_ASYMMETRY = _variant("S01_specificity_asymmetry", _set(
    ["sources", "B", "content"],
    "On the bundled wall charger, the Veltro K7 power bank requires 4 hours "
    "to go from empty to full."))

# Not flagged either: a P1 that names the truth and a distractor outright.
SCREEN_NAMES_OPTIONS = _variant("S02_screen_names_options", _set(
    ["screen_partial"],
    "The Veltro K7 power bank goes from empty to full in either 3 hours or 4 hours."))

CASES = {cid: _variant(cid, edit) for cid, _, edit in _PLANTS}
EXPECTED = {cid: rules for cid, rules, _ in _PLANTS}
for _clean in (SPEC_ASYMMETRY, SCREEN_NAMES_OPTIONS):
    CASES[_clean["case_id"]] = _clean
    EXPECTED[_clean["case_id"]] = set()
