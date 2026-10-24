"""M11: Equipment-kit collection counter at fictional Alderwick University.

Institutional logistics domain, directness dimension, tier T1.
Tests firsthand versus secondhand knowledge of a collection location.
"""

CASE = {
    "case_id": "M11",
    "domain": "institutional_logistics",
    "question": (
        "Which counter is assigned for collecting engineering laboratory "
        "equipment kits at Alderwick University?"
    ),
    "world_truth": "Counter C",
    "distractors": ["Counter A", "Counter D"],
    "screen_partial": (
        "The assigned collection counter at Alderwick University "
        "is alphabetically after Counter A and before Counter D."
    ),
    "quality_dimension": "directness",
    "difficulty_tier": "T1",

    "design_notes": (
        "M11 tests directness using conflicting collection-counter "
        "assignments for engineering laboratory equipment kits at "
        "fictional Alderwick University. Source A claims Counter B, "
        "while Source B supports the true assignment of Counter C. "
        "Both concern the same kits, collection activity and location "
        "without exceptions or changes (R1). "
        "A is a secondhand account from a staff member who missed "
        "the organisers' briefing, whereas B is a firsthand account "
        "from an equally ranked staff member who attended it. "
        "Both have the same authority, isolating directness (R19). "
        "A uses the mild clause-level hedge 'is thought to be', "
        "which is intended to survive paraphrasing (R16). "
        "If the hedge disappears from frozen reports, relabel T2. "
        "Source identity and evidence methods remain in provenance "
        "rather than content (R2). A and B describe the same "
        "question-related concepts (R13). B, C and D support "
        "Counter C using different sentence frames (R17). "
        "C and D provide separate firsthand observations of the "
        "collection location rather than copying B's briefing account. "
        "Their independence and consistency with the assigned counter "
        "must be assessed during manual review (R6, A7). "
        "The four counters are consecutive alphabetical alternatives, "
        "with both competing claims in the interior positions (R8). "
        "The screen preserves Counter B and Counter C while excluding "
        "Counter A and Counter D (R15). "
        "Three filler sets describe distinct campus settings without "
        "equipment collection details or source-identifying language "
        "(R9, R10, R12). Filler and source lengths must pass R20."
    ),

    "filler_sets": [
        [
            "The university arts centre has a broad entrance framed by tall pale stone pillars outside.",
            "A tiled foyer contains upholstered benches and large paintings mounted along the walls.",
            "Tall glass panels overlook a courtyard filled with ornamental shrubs and smooth pebbles.",
            "A sculptural metal installation stands beside the staircase, with curved pieces forming an abstract pattern.",
            "The ceiling has recessed lighting fixtures, while a woven carpet covers the centre of the spacious foyer near the main entrance doors.",
        ],
        [
            "The campus sports hall has a wooden floor bordered by pale walls.",
            "Folded bleachers rest against the far wall beside neatly stacked protective mats.",
            "High windows admit daylight through frosted glass, and large ceiling fans hang from exposed beams.",
            "A storage alcove contains exercise cones, wheeled carts and folded fabric covers.",
            "The entrance corridor has rubber flooring, a drinking fountain and colourful geometric murals extending along the walls toward the main indoor court and the adjoining recreation area.",
        ],
        [
            "The campus dining hall contains wooden tables surrounded by chairs with upholstered seats.",
            "Decorative pendant lamps hang above the central seating area beneath a high ceiling.",
            "Large windows face an outdoor terrace with ceramic planters and small ornamental trees.",
            "The walls feature framed illustrations of local landmarks, while tiled flooring extends across the open space.",
            "A broad passage leads toward the entrance, with a decorative partition separating the dining area from an adjacent sheltered walkway beside the courtyard.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "Counter B",
            "provenance": {
                "type": "summary relayed by a staff member absent from the briefing",
                "authority": "university support staff",
                "quality": "weak",
                "why": (
                    "The staff member received the information from "
                    "a colleague rather than hearing the organisers' "
                    "announcement directly."
                ),
            },
            "content": (
            "Collecting engineering laboratory equipment kits at Alderwick University "
            "is thought to be assigned Counter B."
        ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "Counter C",
            "provenance": {
                "type": "notes made by a staff member present at the briefing",
                "authority": "university support staff",
                "quality": "strong",
                "why": (
                    "The staff member personally attended the briefing "
                    "and heard the organisers announce the collection location."
                ),
            },
            "content": (
                "At Alderwick University, Counter C is assigned "
                "for collecting engineering laboratory equipment kits."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "Counter C",
            "provenance": {
                "type": "onsite collection observation",
                "authority": "university support staff",
                "quality": "strong",
                "why": (
                    "A separate staff member personally observed "
                    "the designated counter being used for kit collection "
                    "without consulting B's briefing notes."
                ),
            },
            "content": (
                "Counter C serves as the engineering laboratory "
                "equipment kit collection point at Alderwick University."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "Counter C",
            "provenance": {
                "type": "firsthand collection duty record",
                "authority": "university support staff",
                "quality": "strong",
                "why": (
                    "Another staff member independently recorded the "
                    "counter where they personally distributed the kits, "
                    "without relying on the other accounts."
                ),
            },
            "content": (
                "Students at Alderwick University collect their "
                "engineering laboratory equipment kits at Counter C."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
