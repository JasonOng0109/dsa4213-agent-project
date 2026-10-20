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
        "The Northwood Lecture Theatre has a seating capacity of less than 260 seats."
    ),  # true, keeps 205 and 240 (truth), rules out 275 and 310
    "quality_dimension": "authority",
    "difficulty_tier": "T1",
    "design_notes": (
        "Authority dimension, T1. A and B state the same proposition (number of seats in the "
        "Northwood Lecture Theatre) as single sentences naming the same scope. Both omit "
        "'seating' and 'capacity', so they share exactly the same set of question content-words "
        "(R13). The T1 cue is A's clause-level hedge 'is reckoned to contain' (R16), against B's "
        "flat assertion. A and B use different frames (R17): "
        "A subject-first with a hedge, B number-first and passive. Quality lives only in "
        "provenance (R2, R19): a student society orientation guide against a university estates space "
        "audit register. C and D state the truth in their own frames without naming their document types (R2)."
        "Content lengths are A=13 and B=13 words. Each filler set is 77-79 words. Filler is plain physical "
        "building upkeep rather than administrative wording (R10), carries no time markers (R3), "
        "no option values, and none of the words that occur only in a source's provenance type."
    ),
    "filler_sets": [
        [
            "Tall windows along the east corridor reflect light paving and square ceiling lights.",
            "The main staircase has broad steps, a dark wooden rail, and a landing beside glass entrance doors.",
            "Metal cabinets stand beneath the plant room windows, with coloured labels on their doors.",
            "The paved courtyard contains low planters, grey walls, and a covered passage linking two building entrances nearby.",
            "A roofline follows the upper edge of the building, above long windows and a projecting concrete canopy overhead.",
        ],
        [
            "Ventilation grilles above the main entrance form narrow horizontal lines across the upper wall.",
            "Fire doors along the west corridor have dark panels and square viewing windows.",
            "The south wall has a long gutter beneath the roof edge and several evenly spaced metal brackets.",
            "A workshop cabinet has labelled drawers, a smooth grey surface, and two handles set near its centre.",
            "Flagpoles at the front entrance rise beside a stone path and a pair of low brick pillars.",
        ],
        [
            "Concrete paths around the northern lawn form straight pale strips between clipped grass and low shrubs.",
            "Emergency torches sit in shallow wall boxes with clear covers and small dark switches.",
            "Radiators in the lower corridors run beneath windows, with valves at either end of each unit.",
            "Heavy rubber mats lie beside side entrances, separated from the wall by strips of tile along the wall.",
            "Water fountains near the cloakroom have curved metal taps, shallow basins, and tiled entrance surrounds.",
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
                "why": "informal handbook compiled by student club members rather than university facilities officers",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "240 seats",
            "content": (
                "Inside the Northwood Lecture Theatre, there are 240 seats installed altogether."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "university estates space audit register",
                "authority": "institutional",
                "quality": "strong",
                "why": "the governing administrative register recording certified building floor plans and safety occupancy limits",
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
                "authority": "institutional",
                "quality": "strong",
                "why": "academic scheduling database used by the central registrar for lecture bookings",
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
                "authority": "institutional",
                "quality": "strong",
                "why": "blueprint specifications drawn and certified by licensed chartered facility architects",
            },
        },
    },
}