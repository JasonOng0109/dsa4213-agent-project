"""M16: Laptop loan period at Ravenscar Hall.

Institutional logistics domain, primary-source quality dimension, tier T1.
"""

CASE = {
    "case_id": "M16",
    "domain": "institutional_logistics",
    "question": "What is the laptop loan period at Ravenscar Hall?",
    "world_truth": "22 days",
    "distractors": ["12 days", "27 days"],  # options: [12, 17, 22, 27]
    "screen_partial": (
        "The laptop loan period at Ravenscar Hall is between 15 days and 24 days."
    ),  # keeps 17 and 22 (truth); rules out 12 and 27; both survivors sit 2 days inside bounds (R15)
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",
    "design_notes": (
        "Primary-source dimension, T1. A and B state the same proposition (the laptop loan "
        "period at Ravenscar Hall) as flat single sentences with the same scope (R1). Both "
        "contain exactly the same five question content-words: laptops, loan, period, Ravenscar "
        "and Hall (R13). The T1 cue is A's clause-level hedge 'are understood to have' (R16), against "
        "B's flat assertion. This hedge is now used 3 times across all cases (used by M2 M3 and M16). "
        "Quality lives only in provenance (R2, R19) and only the primary-source dimension "
        "differs: both writers are the same hall office (same authority value), A's type is "
        "the hall's website summary of its lending terms and B's is the hall's own rulebook, "
        "the document where they are set. Neither name says how the figure was found, how close "
        "its writer was, or that one outranks the other, and neither contains 'independent'. "
        "Type words are not subject words (R2a): no 'loan', 'lending' or 'laptop'. "
        "B, C and D each have their own origin so A7 does not read as one source three times: "
        "B is the hall's rulebook, C is the warden's own notes taken at the committee vote that "
        "set the period, kept apart from the minutes the rulebook was drafted from, and D is the "
        "union representative's notes taken at that same vote, not from the rulebook or minutes. "
        "None of the whys says one source copies another. "
        "Options are 12, 17, 22 and 27 days, evenly spaced so that 'closest to the mean' does "
        "not favour the truth, with the truth and A's claim both interior (R8). The screen "
        "sentence uses two bounds (15 and 24 days), placing both survivors (17 and 22) exactly "
        "2 days inside their respective bounds (R15). "
        "Content lengths are A=14 and B=13 words (R20). Each filler set is 78 or 79 words, so "
        "filler+A and filler+B are 91 to 93 words, within the 91-93 band (R20). Filler "
        "is plain factual description of the hall's building, its common room and its grounds, "
        "one scene per set, each with its own vocabulary so reports in one trial do not repeat "
        "features across slots (R12). It is one plain register with no insider or "
        "administrative wording, no story-like narration, no damage, wear or age wording, no "
        "document-type words, no time markers, no numbers, and nothing about borrowing (R3, R9, "
        "R10). It contains none of the words that occur only in a source's provenance type (R2a). "
        "When reading the frozen reports in step 3.4, check that rewordings still give the "
        "loan period itself, not 'up to' or 'with renewals'."
    ),
    "filler_sets": [
        [
            "The building is faced with red brick walls and topped by a slate tiled roof.",
            "Tall sash windows with white frames are set evenly along the front, on every level.",
            "A central porch with fluted stone pillars protects an oak door painted a dark blue.",
            "Iron railings run along the street edge, and a brass bell hangs beside the porch.",
            "Brick chimney stacks rise from the ridge, each topped with a round clay pot and a metal cap.",
        ],
        [
            "The common room has green fabric sofas arranged in a ring around a low ash stool.",
            "Shelves cover the whole alcove opposite the fireplace and hold board games, jigsaw boxes, and plants.",
            "A woven grey rug with a diamond pattern covers most of the floorboards.",
            "Cushions in orange and yellow lie along the bay seat, and a standard lamp stands beside it.",
            "Watercolours of nearby hills are mounted above the sofas, and a leafy fern fills a corner tub.",
        ],
        [
            "A gravel drive curves from the gate between long flowerbeds of lavender and roses.",
            "Behind the house, a broad lawn slopes down to a reedy pond with a timber jetty.",
            "Apple trees grow in the orchard, with a wooden bench encircling the largest trunk.",
            "A bicycle shelter with a sloping tin canopy sits near the side gate beside a holly hedge.",
            "A narrow footpath of packed earth leads beyond the shelter to a vegetable garden with raised beds.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "17 days",
            "content": (
                "At Ravenscar Hall, laptops are understood to have a loan period of 17 days."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "hall website summary",
                "authority": "hall office",
                "quality": "weak",
                "why": "a web page on the hall's own site that restates the lending terms for readers, rather than being the place where they are set",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "22 days",
            "content": (
                "Ravenscar Hall lends out its laptops for a loan period lasting 22 days."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "hall rulebook",
                "authority": "hall office",
                "quality": "strong",
                "why": "the hall's own rulebook, the document in which the hall sets out its lending terms",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "22 days",
            "content": (
                "A Ravenscar Hall laptop has a loan period of 22 days."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "warden's own notes",
                "authority": "hall warden",
                "quality": "strong",
                "why": "notes the hall warden took at the committee vote that set the laptop loan period, kept apart from the minutes the rulebook was drafted from",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "22 days",
            "content": (
                "At Ravenscar Hall, the loan period for a laptop is twenty-two days."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "union representative's notes",
                "authority": "student union representative",
                "quality": "strong",
                "why": "notes the student union's representative took at the committee vote that set the laptop loan period, not from the rulebook or the minutes",
            },
        },
    },
}