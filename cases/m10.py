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
        "This case tests authority using conflicting guest-pass allowances at the fictional "
        "Westbridge University library. Source A claims 4 passes, while Source B supports the "
        "true allowance of 3 passes. A and B concern the same students, library and "
        "allowance, with no changes or exceptions, and neither states its scope more fully "
        "than the other (R1). Authority only: both type names are websites, so the kind of "
        "document is the same and only the writer's standing differs, a student society "
        "against the library administration that sets the allowance (R19). Source A uses the "
        "clause-level hedge 'is guessed to have permission to request' (R16), shared with "
        "M28; 'is thought to' was already on more than three T1 cases. The T1 label must be "
        "checked against the frozen reports and relabelled T2 if the hedge disappears. Source "
        "identity and authority remain in provenance rather than content (R2). The answer "
        "options are 2, 3, 4 and 5 passes, placing both competing claims in the interior "
        "positions (R8). The screen sentence keeps 3 and 4 passes, each one step inside a "
        "bound, and excludes 2 and 5 (R15). B, C and D each reach the figure by their own "
        "route (A7): B is the administration that sets the allowance, C the access services "
        "office applying it in its own guest-entry procedures, and D the visitor desk's own "
        "log of passes issued, which stops each student at the limit. B, C and D use "
        "different sentence frames (R17). The filler describes the library's front, its "
        "reading room and the garden behind it, in plain one-fact sentences with no content "
        "word in two sets, and says nothing about guests, passes, entry or rules (R9, R10, "
        "R12). Each filler set is 77 words and A and B are 16 words each, so long reports "
        "are 93 words (R20)."
    ),

    "filler_sets": [
        [
            "The Westbridge University library stands at the head of a broad lawn.",
            "Its front is faced in honey-coloured limestone.",
            "Tall pillars hold up a triangular pediment over the entrance.",
            "A carved stone owl perches at the very peak of the pediment.",
            "Wide stone steps rise between bronze lamp standards to the doors.",
            "The doors are of dark oak with iron studs.",
            "Ivy softens the corners of the building.",
            "A flagpole flies the university's crest beside the steps.",
        ],
        [
            "The main reading room sits beneath a high domed ceiling.",
            "Painted panels of blue sky and white clouds fill the dome.",
            "Arched windows let daylight fall across long walnut tables.",
            "Green glass shades cover the reading lights on each table.",
            "Galleries with brass railings run around the upper walls.",
            "Spiral staircases climb to the galleries from the floor.",
            "Plaster garlands decorate the frieze below the dome.",
            "The floor is laid with patterned tiles in red and cream.",
        ],
        [
            "Behind the library lies a sunken garden.",
            "Gravel paths cross its beds of herbs.",
            "A veined marble fountain plays in the middle.",
            "Clipped yew hedges enclose the garden.",
            "A pergola of rambling roses shelters a teak bench.",
            "Lavender and rosemary edge the herb beds.",
            "Goldfish swim in a lily pond near the gate.",
            "A mulberry tree spreads its branches over the pond.",
            "Wrens and robins nest in the hedges.",
            "Moss grows between the flagstones of a terrace.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "4 passes",
            "provenance": {
                "type": "student society website",
                "authority": "student society",
                "quality": "weak",
                "why": (
                    "The website is run by a student society with no say "
                    "over library access rules."
                ),
            },
            "content": (
                "Each student is guessed to have permission to request "
                "4 guest passes for Westbridge University library."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "3 passes",
            "provenance": {
                "type": "library administration website",
                "authority": "university library administration",
                "quality": "strong",
                "why": (
                    "The library administration sets the guest-pass allowance "
                    "and publishes it on its own website."
                ),
            },
            "content": (
                "For the Westbridge University library, the number of guest "
                "passes each student may request is 3."
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
                "type": "visitor desk issue log",
                "authority": "library visitor desk",
                "quality": "strong",
                "why": (
                    "Staff at the visitor desk log every guest pass they "
                    "issue and stop each student at the limit, so the log "
                    "shows the rule being applied."
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
