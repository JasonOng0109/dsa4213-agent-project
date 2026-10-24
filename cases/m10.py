"""M10: Guest-pass allowance at the fictional Westbridge University library.

Institutional logistics domain, authority dimension, tier T1.
Tests conflicting guest-pass limits from sources with different authority.
"""

CASE = {
    "case_id": "M10",
    "domain": "institutional_logistics",
    "question": (
        "How many guest passes may each student request for "
        "the Westbridge University library?"
    ),
    "world_truth": "3 passes",
    "distractors": ["2 passes", "5 passes"],
    "screen_partial": (
        "Each student may request more than 2 but fewer than 5 guest passes "
        "for the Westbridge University library."
    ),
    "quality_dimension": "authority",
    "difficulty_tier": "T1",

    "design_notes": (
        "This case tests authority using conflicting guest-pass allowances "
        "at the fictional Westbridge University library. Source A claims "
        "4 passes while Source B supports the true allowance of 3 passes. "
        "A and B concern the same student, library and request allowance, "
        "with no changes or exceptions (R1). A is a student-run campus "
        "information page, while B is a library administration notice. "
        "Both directly state the policy, but only B has recognised "
        "responsibility for setting library access rules (R19). "
        "Source A uses the mild hedge 'is thought to have permission to request', "
        "which should survive faithful paraphrasing (R16). The T1 "
        "classification must be checked against frozen reports and "
        "relabelled T2 if the hedge disappears. Source identity and "
        "authority remain in provenance rather than content (R2). "
        "The answer options are 2, 3, 4 and 5 passes, placing both "
        "competing claims in the interior positions (R8). The screen "
        "sentence retains 3 and 4 passes while excluding 2 and 5 "
        "(R15). Sources B, C and D use different sentence structures "
        "while supporting the same allowance (R17). Their evidence "
        "origins must be checked for independence before A7 is "
        "interpreted as three independent confirmations. "
        "The filler sets describe distinct campus locations without "
        "guest-pass information, library rules or source-identifying "
        "language (R9, R10, R12). Filler and source lengths must "
        "be verified against R20 before submission."
    ),

    "filler_sets": [
        [
            "The campus arts building has a broad entrance framed by pale stone pillars.",
            "A tiled foyer contains upholstered benches and several large paintings mounted along the walls.",
            "Tall glass panels overlook a landscaped courtyard filled with decorative shrubs and smooth pebbles.",
            "A sculptural metal installation stands beside the staircase, with curved pieces forming an abstract pattern.",
            "The ceiling has recessed lighting fixtures, while a woven carpet covers the centre of the spacious foyer near the entrance doors.",
        ],
        [
            "The university sports complex has an indoor court with wooden flooring and painted boundary markings.",
            "Folded bleachers rest against the far wall beside neatly stacked protective mats.",
            "High windows admit daylight through frosted glass, and large ceiling fans hang from exposed beams.",
            "A storage alcove contains exercise cones, wheeled equipment carts and folded fabric covers.",
            "The entrance corridor has rubber flooring, a drinking fountain and colourful geometric murals extending along the walls toward the main indoor hall.",
        ],
        [
            "The campus dining hall contains wooden tables surrounded by chairs with dark upholstered seats.",
            "Decorative pendant lamps hang above the central seating area, suspended from a high ceiling.",
            "Large windows face an outdoor terrace with ceramic planters and small ornamental trees.",
            "The walls feature framed illustrations of local landmarks, while tiled flooring extends across the open space.",
            "A broad passage leads toward the entrance, with a decorative partition separating the dining area from the adjacent sheltered walkway.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "4 passes",
            "provenance": {
                "type": "student-run campus information page",
                "authority": "student contributors",
                "quality": "weak",
                "why": (
                    "The page is maintained by students who have no "
                    "institutional responsibility for library access rules."
                ),
            },
        "content": (
            "Each student is thought to have permission to request "
            "4 guest passes for Westbridge University library."
        ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "3 passes",
            "provenance": {
                "type": "university library administration notice",
                "authority": "university library administration",
                "quality": "strong",
                "why": (
                    "The library administration has recognised responsibility "
                    "for establishing the university's guest-pass allowance."
                ),
            },
            "content": (
                "For Westbridge University library, each student may "
                "request a total of 3 guest passes."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "3 passes",
            "provenance": {
                "type": "campus access services policy confirmation",
                "authority": "university access services",
                "quality": "strong",
                "why": (
                    "The access services office independently confirms "
                    "the allowance through its own guest-entry procedures."
                ),
            },
            "content": (
                "Three guest passes are available per student "
                "for the Westbridge University library."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "3 passes",
            "provenance": {
                "type": "university visitor services guidance",
                "authority": "university visitor services",
                "quality": "strong",
                "why": (
                    "Visitor services maintains its own operational "
                    "confirmation of the guest-pass limit."
                ),
            },
            "content": (
                "The Westbridge University library permits each "
                "student to request 3 guest passes."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
