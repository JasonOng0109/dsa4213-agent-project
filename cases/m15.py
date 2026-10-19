"""M15: Seating capacity of the Northwood Lecture Theatre.

Institutional logistics domain, authority quality dimension, tier T1.
"""

CASE = {
    "case_id": "M15",
    "domain": "institutional_logistics",
    "question": "What is the seating capacity of the Northwood Lecture Theatre?",
    "world_truth": "240 seats",
    "distractors": ["180 seats", "310 seats"],  # options: [180, 240, 275, 310]
    "screen_partial": (
        "The Northwood Lecture Theatre has a seating capacity of less than 260 seats."
    ),  # true, keeps 180 and 240 (truth), rules out 275 and 310: exactly half
    "quality_dimension": "authority",
    "difficulty_tier": "T1",
    "design_notes": (
        "Authority dimension, T1. A and B state the same proposition (number of seats in the "
        "Northwood Lecture Theatre) as single sentences naming the same scope. Both omit "
        "'seating' and 'capacity', so they share exactly the same set of question content-words "
        "(R13); the previous A contained both words and B neither. The T1 cue is A's clause-level "
        "hedge 'is believed to hold' (R16), against B's flat assertion. A and B use different frames (R17): "
        "A subject-first with a hedge, B number-first and passive. Quality lives only in "
        "provenance (R2, R19): a student society orientation guide against a university estates space "
        "audit register. C and D state the truth in their own frames without naming their document types (R2)."
        "Content lengths are A=13 and B=13 words. Each filler set is 79 words. Filler is plain physical "
        "building upkeep rather than administrative wording (R10), carries no time markers (R3), "
        "no option values, and none of the words that occur only in a source's provenance type."
    ),
    "filler_sets": [
        [
            "Window frames along the east corridor are cleaned with extendable poles and long soft brushes.",
            "Handrails on the main staircase are polished and checked for loose fixings and worn treads.",
            "Spare light fittings and cable ties are kept in a locked cupboard near the plant room.",
            "Outdoor benches beside the paved courtyard are repainted whenever the colour begins to peel away.",
            "Rainwater from the main roof runs through downpipes into drains that lead to a large underground storage tank.",
        ],
        [
            "Ventilation grilles above the main entrance doors are brushed clean using a soft vacuum attachment.",
            "Fire doors along the west corridor close automatically and are fitted with strong brass hinges.",
            "Gutters on the south side are cleared of leaves and held to the wall by steel brackets.",
            "Spare door handles and hinge pins are stored in labelled drawers inside the workshop cabinet.",
            "Flagpoles at the front entrance are fitted with rope cleats and weighted bases to keep them steady.",
        ],
        [
            "Concrete paths around the northern lawn are swept clear of gravel and brushed with stiff brooms.",
            "Emergency torches are kept in wall boxes and checked for working batteries and loose lenses.",
            "Radiators in the lower corridors are bled, and their valves are turned to a steady setting.",
            "Heavy rubber mats at the side entrances catch mud and are lifted out to be hosed down.",
            "Water fountains near the cloakroom are fitted with filters and small steel drip trays underneath.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "275 seats",
            "content": (
                "The Northwood Lecture Theatre is believed to hold a total of 275 seats."
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
                "Two hundred and forty seats are installed within the Northwood Lecture Theatre altogether."
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