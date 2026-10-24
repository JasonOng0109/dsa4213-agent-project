"""M17: Package holding limit at Highfield Parcel Centre.

Institutional logistics domain, directness quality dimension, tier T1.
"""

CASE = {
    "case_id": "M17",
    "domain": "institutional_logistics",
    "question": "What is the package holding limit at Highfield Parcel Centre?",
    "world_truth": "19 days",
    "distractors": ["13 days", "22 days"],  # [13, 16, 19, 22]
    "screen_partial": (
        "The package holding limit at Highfield Parcel Centre is between 15 days and 20 days."
    ),  # keeps 16 and 19 (truth); rules out 13 and 22; both survivors sit 1 day inside bounds (R15)
    "quality_dimension": "directness",
    "difficulty_tier": "T1",
    "design_notes": (
        "Directness dimension, T1. A and B state the same proposition (the package holding "
        "limit at Highfield Parcel Centre) as single sentences with identical scope (R1). "
        "Both contain exactly the same six question content-words: package, holding, limit, "
        "Highfield, Parcel and Centre (R13). The T1 cue is A's clause-level hedge "
        "'is presumed to be' (R16), against B's flat assertion. This hedge is now used by M7, M17 and M32. "
        "Quality lives only in provenance (R2, R19) and only the directness dimension differs: "
        "both writers are couriers with the same standing (authority 'individual'). A's type is "
        "a summary passed on by a courier who missed the intake briefing, and B's is notes taken "
        "at the intake desk by a courier who was at the briefing. A's why says the figure was "
        "heard from another courier instead of being recorded at the briefing itself, and B's "
        "why says the notes were written at the desk while the briefing took place. Neither "
        "type name says how the figure was found beyond that, or contains 'independent'. "
        "Sources A and B use different frames (R17): A is possessive-fronted with the hedge, B "
        "is plural-noun-fronted ('Packages at ... are stored for'). C and D are written as "
        "plain statements of the rule in their own frames: C is centre-fronted with an active "
        "verb ('sends back any package left uncollected'), D is article-fronted ('An "
        "uncollected package at ... goes back to its sender'). Neither names a document, a "
        "writer or a method, and both name the centre, so each is self-contained (R2, R6, R7). "
        "Their routes sit in provenance only. B, C and D reach the figure separately (A7): B "
        "is a courier's notes from the briefing, C is the centre manager's own notes taken when "
        "the holding limit was set and kept apart from the briefing material, and D is a "
        "consumer group's log of test parcels it left uncollected at the centre. None of the "
        "whys says one source copies another. "
        "Options are 13, 16, 19 and 22 days, evenly spaced so that 'closest to the mean' does "
        "not favour the truth, with the truth (19) and A's claim (16) both interior (R8). The "
        "screen sentence has two bounds, 15 and 20 days, and keeps 16 and 19 (the survivors "
        "are each 1 day inside a bound) while ruling out 13 and 22 (R15). "
        "Content lengths are A=14 and B=14 words (R20). Each filler set is 78 words, so "
        "filler+A and filler+B are both 92, inside the 91-93 band. Filler describes three "
        "separate places in plain factual sentences (the yard behind the building, the entrance "
        "hall, the front grounds), one register throughout (R10). A script check found no stem "
        "shared across two sets apart from function words, so reports in one trial do not "
        "repeat features across slots (R12). Filler has no numbers, time markers, option "
        "values or holding-limit vocabulary, and none of the words that occur only in a "
        "source's provenance type (R2a, R3, R9)."
    ),

    "filler_sets": [
        [
            "The yard behind the building has a concrete surface painted with yellow lines.",
            "Several loading bays open onto the gate, with rubber buffers bolted beside each bay.",
            "A floodlight on a steel mast stands at one corner of the yard.",
            "Bollards line the edge of a ramp, and a drainage grille crosses the approach to the gate.",
            "A coil of hose lies on a bracket next to an outdoor tap close to the ramp and the yard drain.",
        ],
        [
            "The entrance hall has a tiled floor in a chequered pattern and a coir mat by the door.",
            "A staircase with a brass handrail rises to a landing lit by a glass globe.",
            "Coat hooks are fixed beside the door, and an umbrella holder keeps a few umbrellas.",
            "A mirror is mounted above a radiator, and a potted fern fills the space between them.",
            "A pair of chairs with cushions is placed opposite the staircase near the mat.",
        ],
        [
            "A lawn stretches from the road to a gravel path that curves toward the steps.",
            "Rose bushes grow in beds beside the path, and a holly hedge borders the lawn.",
            "A bench with iron arms looks over a birdbath in the middle of the lawn.",
            "Maple trees shade the pavement by the road, and a lamp post marks the start of the path.",
            "A timber fence runs along the boundary, and a water butt sits under a downpipe.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "16 days",
            "content": (
                "Highfield Parcel Centre's holding limit for a package is presumed to be 16 days."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "summary passed on by a courier who missed the intake briefing",
                "authority": "individual",
                "quality": "weak",
                "why": "second-hand information heard from another courier rather than recorded at the intake briefing itself",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "19 days",
            "content": (
                "Packages at Highfield Parcel Centre are stored for a holding limit of 19 days."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "notes taken at the intake desk by a courier at the briefing",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand notes written at the intake desk by a courier while the briefing took place",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "19 days",
            "content": (
                "Highfield Parcel Centre sends back any package left uncollected after 19 days."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "centre manager's own notes",
                "authority": "centre manager",
                "quality": "strong",
                "why": "notes the centre manager took when the holding limit was set, kept apart from the briefing material",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "19 days",
            "content": (
                "An uncollected package at Highfield Parcel Centre goes back to its sender after 19 days."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "consumer group test report",
                "authority": "consumer group",
                "quality": "strong",
                "why": "a consumer group sent test parcels to the centre, left them uncollected and logged the day each was returned once the holding limit ran out",
            },
        },
    },
}