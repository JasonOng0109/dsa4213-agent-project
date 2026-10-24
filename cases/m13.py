"""M13: Number of lanes closed at fictional Bellmere Junction.

Incident status domain, primary-source dimension, tier T1.
Tests conflicting lane-closure counts from original and secondary records.
"""

CASE = {
    "case_id": "M13",
    "domain": "incident_status",
    "question": (
        "How many lanes were closed at Bellmere Junction "
        "following the traffic incident?"
    ),
    "world_truth": "3 lanes",
    "distractors": ["2 lanes", "5 lanes"],
    "screen_partial": (
        "More than 2 but fewer than 5 lanes were closed "
        "at Bellmere Junction following the traffic incident."
    ),
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",

    "design_notes": (
        "M13 tests primary-source quality using conflicting lane-closure "
        "counts following a fictional traffic incident at Bellmere Junction. "
        "Source A claims 4 lanes, while Source B supports the true value "
        "of 3 lanes. Both describe the same initial closure decision "
        "following the same incident, with equally specific claims and "
        "no changes or exceptions (R1). "
        "Source A is a secondary traffic information summary, while "
        "Source B is the original traffic operations record. Both are "
        "maintained by the same transport authority, isolating "
        "primary-source status rather than institutional authority (R19). "
        "Source A contains the mild hedge 'is believed to have', "
        "intended to survive faithful paraphrasing (R16). "
        "If the hedge disappears from frozen reports, the case "
        "will be relabelled T2. "
        "Source identities and evidence-production methods remain "
        "in provenance rather than content (R2). "
        "A and B describe the same question-related property (R13). "
        "Sources B, C and D support 3 lanes using distinct sentence "
        "frames (R17). C and D are firsthand incident observations "
        "that do not copy B's operations record. Their independence "
        "and consistency with the initial closure decision require "
        "manual verification (R6, A7). "
        "The four options are 2, 3, 4 and 5 lanes, evenly spaced "
        "with both competing claims in the interior positions (R8). "
        "The screening sentence preserves 3 and 4 lanes while "
        "excluding 2 and 5 lanes (R15). "
        "The three filler sets describe distinct physical areas "
        "around the junction without discussing lane closures, "
        "traffic restrictions or source-identifying information "
        "(R9, R10, R12). "
        "Filler and source lengths must be checked against R20."
    ),

    "filler_sets": [
        [
            "The pedestrian plaza beside Bellmere Junction has broad stone paving and decorative curved metal benches.",
            "Several ornamental trees stand near the edge of the square, surrounded by circular planters.",
            "The adjoining building has a glass entrance framed by pale stone panels.",
            "Small flower beds add colour beside the walkway, while a sculptural fountain occupies the centre of the open space.",
            "The plaza has low walls with smooth tops, and several large ceramic pots sit near the entrance.",
        ],
        [
            "A public garden near Bellmere Junction contains paths bordered by trimmed hedges and flowering shrubs.",
            "Wooden benches face a shallow pond with smooth stones arranged along its edge.",
            "Tall trees shade the central lawn, while decorative lanterns stand beside the garden paths.",
            "A small pavilion has a tiled roof supported by wooden posts and surrounded by ornamental plants.",
            "The garden entrance features a curved archway with climbing vines, and a gravel path leads toward the shaded seating area.",
        ],
        [
            "The community building near Bellmere Junction has a wide foyer with polished tiled flooring.",
            "Framed landscape photographs hang along the walls above several upholstered visitor chairs.",
            "A wooden reception counter faces the entrance, with a decorative plant beside its corner.",
            "Large windows overlook a courtyard containing stone planters and a small ornamental tree.",
            "The ceiling has recessed lighting fixtures, while a woven rug covers part of the floor near the entrance doors and the adjoining seating area.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "4 lanes",
            "provenance": {
                "type": "secondary traffic information summary",
                "authority": "municipal transport authority",
                "quality": "weak",
                "why": (
                    "The summary reproduces closure information "
                    "from other records rather than originating "
                    "the initial incident decision."
                ),
            },
            "content": (
                "Following the traffic incident, 4 lanes are believed "
                "to have been closed at Bellmere Junction."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "3 lanes",
            "provenance": {
                "type": "original traffic operations record",
                "authority": "municipal transport authority",
                "quality": "strong",
                "why": (
                    "The record was created by the transport "
                    "authority personnel responsible for documenting "
                    "the initial lane-closure decision."
                ),
            },
            "content": (
                "Following the traffic incident at Bellmere Junction, "
                "a total of 3 lanes were closed."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "3 lanes",
            "provenance": {
                "type": "onsite incident observation",
                "authority": "municipal transport authority",
                "quality": "strong",
                "why": (
                    "A separate field officer directly observed "
                    "the initial closure at the junction without "
                    "consulting B's operations record."
                ),
            },
            "content": (
                "At Bellmere Junction, 3 lanes were closed "
                "following the traffic incident."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "3 lanes",
            "provenance": {
                "type": "field deployment observation",
                "authority": "municipal transport authority",
                "quality": "strong",
                "why": (
                    "Another field officer independently documented "
                    "the same initial closure from firsthand "
                    "observation rather than copying the other records."
                ),
            },
            "content": (
                "The traffic incident at Bellmere Junction "
                "resulted in the closure of 3 lanes."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
