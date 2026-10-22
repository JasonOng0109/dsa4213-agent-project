"""M15: Seating capacity of the Northwood Lecture Theatre.

Institutional logistics domain, authority quality dimension, tier T1.
"""

CASE = {
    "case_id": "M15",
    "domain": "institutional_logistics",
    "question": "What is the seating capacity of the Northwood Lecture Theatre?",
    "world_truth": "240 seats",
    "distractors": ["205 seats", "310 seats"],  # options: [205, 240, 275, 310]
    "screen_partial": (
        "The Northwood Lecture Theatre has a seating capacity of between 185 and 260 "
        "seats."
    ),  # true, keeps 205 and 240 (truth), rules out 275 and 310
    "quality_dimension": "authority",
    "difficulty_tier": "T1",
    "design_notes": (
        "Authority dimension, T1. A and B state the same proposition (number of seats in the "
        "Northwood Lecture Theatre) as single sentences naming the same scope. Both omit "
        "'seating' and 'capacity', so they share exactly the same set of question content-words "
        "(R13). The T1 cue is A's clause-level hedge 'is reckoned to contain' (R16), against B's "
        "flat assertion. A and B use different frames (R17): "
        "A is subject-first with a hedge, B is location-fronted ('Inside the ... there are'). "
        "Quality lives only in provenance (R2, R19) and only the authority dimension varies: "
        "a student society orientation guide against a university estates space register. "
        "'Audit' was dropped from B's type because it suggests a careful method, and 'certified' "
        "was dropped from B's why for the same reason. A's why says 'written', not 'compiled', "
        "because 'compiled' suggests the information was gathered second-hand, which is a "
        "directness cue. "
        "C and D state the truth in their own frames without naming their document types (R2). "
        "B, C and D each have their own origin so A7 does not read as one source three times: "
        "B is the estates office's own register of the buildings it looks after, C is the "
        "registrar's booking system set up and counted by the registrar's own staff, and D is the "
        "architects' design drawings."
        "Content lengths are A=13 and B=13 words (R20). Each filler set is exactly 79 words, so "
        "filler+A and filler+B are both 92, inside the 91-93 band. Filler describes plain "
        "physical features of the building as three separate scenes (the front of the building, "
        "the entrance lobby, the grounds), each with its own nouns and adjectives, so reports "
        "in one trial do not repeat features across slots (R12). It is written as plain factual "
        "statements in one register, with no insider or administrative wording (R10), no time "
        "markers (R3), no option values, no mention of the theatre or its seats (R9), and none "
        "of the words that occur only in a source's provenance type (R2a)."
    ),
    "filler_sets": [
        [
            "The front of the building is faced with red brick and has a wide stone step at its centre.",
            "A curved metal handrail follows the step on both sides and finishes in a rounded post.",
            "Above the step, a flat concrete canopy projects forward on two thin round pillars.",
            "Round lamps are suspended from the canopy, and a brass plate is fixed to the brickwork.",
            "A narrow bed of lavender runs along the brickwork under a low window sill.",
        ],
        [
            "The lobby has a tiled surface in two shades of grey and an oval rug near the middle.",
            "Several iron hooks are mounted along one tall wooden panel, and an umbrella holder sits beside it.",
            "Pale wooden benches face each other across the rug, each with a slim cushion.",
            "A tall mirror with a white frame hangs above a small shelf holding a glass bowl.",
            "Heavy double doors open onto a short passage lined with potted ferns and chairs.",
        ],
        [
            "A car park of dark asphalt lies to the east, edged by a clipped privet hedge.",
            "Yellow stripes divide the bays, and a bicycle rack stands near the hedge.",
            "A broad lawn slopes gently toward a pond with a timber jetty and an island of reeds.",
            "Three oak trees shade a grassy mound beside the path, and a litter bin stands at its end.",
            "A signpost at the corner of the car park shows the way to the road.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "275 seats",
            "content": (
                "The Northwood Lecture Theatre is reckoned to contain a total of 275 seats."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "student society orientation guide",
                "authority": "individual",
                "quality": "weak",
                "why": "informal handbook written by student club members rather than university facilities officers",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "240 seats",
            "content": (
                "Inside the Northwood Lecture Theatre, there are 240 seats installed throughout the room."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "university estates space register",
                "authority": "institutional",
                "quality": "strong",
                "why": "the governing administrative register kept by the estates office for the buildings it owns and looks after",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "240 seats",
            "content": (
                "Northwood Lecture Theatre offers 240 individual seats across its tiers."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "campus timetabling venue capacity list",
                "authority": "central registrar",
                "quality": "strong",
                "why": "the registrar's own booking system, whose room entries are set up and counted by the registrar's own staff rather than copied from the estates office",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "240 seats",
            "content": (
                "Across the Northwood Lecture Theatre, the seats come to 240 in all."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "campus architectural floor plan",
                "authority": "chartered architects",
                "quality": "strong",
                "why": "drawings prepared by the chartered architects who designed the building, showing the seating layout they specified",
            },
        },
    },
}