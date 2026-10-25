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
        "The ME2103 lab logbook is worth more than a twentieth and less than a fifth of "
        "the final module grade."
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
            "Safety induction is required before students may operate the heavy machines "
            "in the teaching lab downstairs.",
            "Lab coats and goggles are provided by the door, and bags are stowed on wall "
            "racks in the corridor outside.",
            "Faults with the machines go straight to the technician on duty.",
            "Technicians offer drop-in hours alongside each class for questions about the "
            "equipment.",
            "Students repeating the course stay in their usual class unless they ask to "
            "move.",
            "Closed shoes are needed in the lab.",
        ],
        [
            "ME2103 is a core module, and its practicals are run in a long room under "
            "the main hall.",
            "Bench numbers and partner lists are pinned up by the stairs and at the front "
            "desk.",
            "Kit for each experiment is laid out beforehand and returned to the store "
            "afterwards.",
            "Everyone works in pairs, and each person keeps a logbook of their own.",
            "Benches are numbered, and each pair works at the same bench.",
            "Sinks line the far end of the room.",
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
