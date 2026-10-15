"""M1: the weight of the ME2103 lab logbook.

Institutional logistics, authority dimension, tier T2. The proposal's Appendix A shows
this case in condition X3.
"""

CASE = {
    "case_id": "M1",
    "domain": "institutional_logistics",
    "question": "What percentage of the final ME2103 grade comes from the lab logbook?",
    "world_truth": "15%",
    "distractors": ["10%", "30%"],      # plausible, unsupported, same kind as the truth
    "screen_partial": (
        "The ME2103 lab logbook is worth less than a fifth of the final module grade."
    ),   # screen level P1: true, keeps the truth, rules out 25% and 30%
    "quality_dimension": "authority",
    "difficulty_tier": "T2",            # the register cue is a second-person pronoun,
                                        # which paraphrasing drops (R16)
    "design_notes": (
        "A and B state the same proposition with different values, in one sentence each, "
        "naming the same denominator, with no reference to any change or to each other. "
        "The intended cue was register -- A addresses the reader, B does not -- but it does "
        "not survive paraphrasing (R16), so this case runs as T2: near-symmetric, with "
        "no usable cue, a control for whether a dependency note alone discounts the count. "
        "All quality information sits in provenance, which the reporter never sees. B, C "
        "and D state the fact in three different frames so their paraphrases cannot "
        "converge (R17), and the question uses a verb none of the sources use (R13)."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "Logbooks are collected from the mechanical engineering general office and "
            "must be signed by a demonstrator before they leave the laboratory.",
            "Each entry records the apparatus used, the measurements taken and any "
            "deviation from the set procedure.",
            "Entries are made in ink, and loose sheets are pasted into the book rather "
            "than stapled.",
            "Spare logbooks are held at the office counter for anyone who fills one.",
            "Laboratory groups are fixed by the general office, and the basement "
            "workshop is used.",
        ],
        [
            "Safety induction is required before anyone may work with the heavy machines in "
            "the basement workshop.",
            "Laboratory coats and eye protection are provided at the workshop entrance, "
            "and bags are left on the racks outside the working area.",
            "Apparatus faults are reported to the demonstrator on duty rather than to "
            "the department office.",
            "Demonstrator office hours run alongside each laboratory session for "
            "questions about apparatus or procedure.",
            "Groups repeating the module keep their existing session unless a change is "
            "requested.",
        ],
        [
            "ME2103 is a second-year module administered by the mechanical engineering "
            "department, and its laboratory sessions are held in the basement workshop.",
            "Session lists and bench numbers are posted at the workshop entrance and at "
            "the general office.",
            "Equipment for each experiment is set out before the session and returned "
            "to the equipment store afterwards.",
            "Students work in pairs, and each student keeps a logbook of their own.",
            "Benches are numbered, and the same bench is used by a group throughout.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "25%",
            "provenance": {
                "type": "student-run module wiki page",
                "authority": "individual",
                "quality": "weak",
                "why": "compiled by past students from memory, not an official record",
            },
            "content": "The ME2103 lab logbook counts for 25% of your final module grade.",
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "15%",
            "provenance": {
                "type": "ME2103 assessment brief, section 4",
                "authority": "institutional",
                "quality": "strong",
                "why": "the module's own governing document for assessment weighting",
            },
            "content": "The ME2103 lab logbook carries 15% of the final module grade.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "15%",
            "provenance": {
                "type": "faculty assessment schedule table",
                "authority": "institutional",
                "quality": "strong",
                "why": "faculty-level record compiled from approved module briefs",
            },
            "content": ("Of the ME2103 marks available, fifteen per cent are "
                        "awarded for the lab logbook."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "15%",
            "provenance": {
                "type": "module coordinator announcement to enrolled students",
                "authority": "institutional",
                "quality": "strong",
                "why": "issued by the academic responsible for the module",
            },
            "content": ("The lab logbook contributes 15% towards a student's "
                        "overall ME2103 result."),
            "n_paraphrases_needed": 1,
        },
    },
}
