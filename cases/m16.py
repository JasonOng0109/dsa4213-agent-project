"""M16: Laptop loan period at the Ravenscar Hall.

Institutional logistics domain, primary-source quality dimension, tier T1.
"""

CASE = {
    "case_id": "M16",
    "domain": "institutional_logistics",
    "question": "What is the laptop loan period at Ravenscar Hall?",
    "world_truth": "28 days",
    "distractors": ["14 days", "35 days"],  # options: [14, 21, 28, 35]
    "screen_partial": (
        "The laptop loan period at Ravenscar Hall is between 24 days and 39 days."
    ),  # keeps 28 (truth) and 35; rules out 14 and 21; both survivors sit 4 days inside bounds (R15)
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",
    "design_notes": (
        "Primary-source dimension, T1. A and B state the same proposition (the laptop loan "
        "period at Ravenscar Hall) as flat single sentences with the same scope (R1). Both "
        "contain exactly the same five question content-words: laptop, loan, period, Ravenscar "
        "and Hall (R13). The T1 cue is A's clause-level hedge 'is considered to be' (R16), against "
        "B's flat assertion. It varies from 'is understood to' (M2, M3), 'is believed to' (M15) "
        "and 'is presumed to' (M7). A and B use different frames (R17): A is 'The ... period at "
        "... is considered to be', B is plural-noun-fronted ('Laptops at ... are lent for'); C is "
        "'Borrowers may keep ...' and D is place-fronted with a spelled-out number. The entity "
        "name is the only chunk they share. "
        "Quality lives only in provenance (R2, R19) and only the primary-source dimension "
        "differs: both writers are the same hall office (same authority value), A's type is "
        "the hall's website summary of its lending terms and B's is the hall's own rulebook, "
        "the document where they are set. Neither name says how the figure was found, how close "
        "its writer was, or that one outranks the other, and neither contains 'independent'. "
        "Type words are not subject words (R2a): no 'loan', 'lending' or 'laptop'. "
        "B, C and D each have their own origin so A7 does not read as one source three times: "
        "B is the hall's rulebook, C is the equipment supplier's own terms for the leased "
        "laptops, and D is the loan desk's own handout slips. None of the whys says one source "
        "copies another. "
        "Options are 14, 21, 28 and 35 days, evenly spaced so that 'closest to the mean' does "
        "not favour the truth, with the truth and A's claim both interior (R8). The screen "
        "sentence uses two bounds (24 and 39 days), placing both survivors (28 and 35) exactly "
        "4 days inside their respective bounds (R15). "
        "Content lengths are A=13 and B=13 words (R20). Each filler set is exactly 79 words, so "
        "filler+A and filler+B are both 92 words, strictly within the 91-93 band (R20). Filler "
        "is plain factual description of the hall's building, its common room and its grounds, "
        "one scene per set, each with its own vocabulary so reports in one trial do not repeat "
        "features across slots (R12). It is one plain register with no insider or "
        "administrative wording, no story-like narration, no damage, wear or age wording, no "
        "document-type words, no time markers, no numbers, and nothing about borrowing (R3, R9, "
        "R10). It contains none of the words that occur only in a source's provenance type (R2a)."
    ),
    "filler_sets": [
        [
            "The building is faced with warm red brick and topped by a steep slate roof.",
            "Tall sash windows with white frames are set evenly along the front, three on each level.",
            "A central porch with two stone pillars protects a heavy oak door painted deep blue.",
            "Iron railings run along the street edge, and a brass bell hangs beside the porch.",
            "Two chimney stacks rise from the ridge, each topped with a round clay pot and a metal cap.",
        ],
        [
            "The common room has soft green sofas arranged in a ring around a low ash stool.",
            "Shelves cover the long wall opposite the fireplace and hold board games, jigsaw boxes, and plants.",
            "A woven grey rug with a diamond pattern covers most of the floorboards.",
            "Cushions in orange and yellow lie along the bay seat, and a standard lamp stands beside it.",
            "Watercolours of nearby hills are mounted above the sofas, and a leafy fern fills a corner tub.",
        ],
        [
            "A gravel drive curves from the gate between neat flowerbeds of lavender and roses.",
            "Behind the house, a broad lawn slopes down to a reedy pond with a timber jetty.",
            "Four apple trees grow in the orchard, with a bench built around the widest trunk.",
            "A bicycle shelter with a sloping tin canopy sits near the side gate beside a holly hedge.",
            "A narrow footpath of packed earth leads beyond the shelter to a vegetable garden with raised beds.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "21 days",
            "content": (
                "The laptop loan period at Ravenscar Hall is considered to be 21 days."
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
            "claim": "28 days",
            "content": (
                "Laptops at Ravenscar Hall are lent for a loan period of 28 days."
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
            "claim": "28 days",
            "content": (
                "Borrowers may keep a Ravenscar Hall laptop for 28 days."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "supplier lease schedule",
                "authority": "supplier",
                "quality": "strong",
                "why": "the equipment supplier's own terms for the leased laptops, which cap how long a unit may be away from the hall as a condition of its insurance cover",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "28 days",
            "content": (
                "At Ravenscar Hall, a laptop stays on loan for twenty-eight days."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "desk checkout slips",
                "authority": "desk staff",
                "quality": "strong",
                "why": "slips the loan desk staff write out as each laptop is handed over, carrying the return date they set themselves",
            },
        },
    },
}