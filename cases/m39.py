"""M39: how many cars were damaged in the Aldmoor car park fire.

Incident or status reports, directness dimension, tier T1. A's hedge, "is likely to have",
is the one mild cue, and is meant to survive rewording (R16).
"""

CASE = {
    "case_id": "M39",
    "domain": "incident_status",
    "question": "How many cars were damaged in the Aldmoor car park fire?",
    "world_truth": "31 cars",
    "distractors": ["23 cars", "47 cars"],   # plausible, unsupported, same kind as the
                                            # truth; even steps of 8 cars
    "screen_partial": (
        "Between 19 and 35 cars were damaged in the Aldmoor car park fire."
    ),   # screen level P1: true, keeps 23 and 31 cars, each 4 inside a bound, and
         # rules out 39 and 47 cars
    "quality_dimension": "directness",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, how many cars were damaged in the Aldmoor car "
        "park fire, with different values, in one sentence each. Both count cars damaged "
        "in the same fire, give a whole total ('in all', 'altogether'), and refer to no "
        "change and to no other source (R1). Read without provenance, neither is narrower, "
        "an exception to the other, or more precise. The quality dimension, directness, "
        "lives in provenance; the one cue in the content is A's clause-level hedge, 'is "
        "likely to have', a hedge of the size a faithful rewording should keep (R16). "
        "Only M23 used it when this case was written, among the hedges least used then, "
        "and M37 has taken it since ('it is likely that'); if it is lost in the frozen "
        "reports, the case is relabelled T2. B is flat and "
        "carries no cue. The options are 23, 31, 39 and 47 cars, evenly spaced and none "
        "a round number, so the truth and A's claim are both interior and equally close "
        "to the average: neither 'avoid the extremes' nor 'pick the middle' finds the "
        "truth (R8). The screen sentence keeps 23 and 31 cars and rules out 39 and 47 "
        "(R15). The two type names carry the directness dimension and nothing else: both "
        "are stories by a local reporter, one written at the scene and one written from a "
        "reader's phone call, so the writers have the same standing (R19). Neither says "
        "'independent', and both name the source rather than the subject, so no word a "
        "rewording needs is banned (R2a). A and B use the same question words and both "
        "leave out 'many' (R13). B, C and D state the fact in three different frames "
        "(R17). C and D are counts made by others, the fire service that put out the fire "
        "and the car park's operator, so neither depends on the reporter or on each "
        "other, and neither says how its value was found (R2, R6). All three whys count "
        "every car the fire damaged, so B, C and D support one proposition in A7 (R1). "
        "The car park and the "
        "fire are invented (R4). Filler describes the car park building, the street "
        "outside it and the town around it, with nothing about the fire, damage, cars, "
        "parking spaces or how full the car park was, no figures and no second person. "
        "It describes what anyone could see on a map or a postcard, so no slot implies "
        "that its writer was there (R3, R9, R10), and no distinctive word is in more than "
        "one set (R12). Each filler set is 79 words and A's and "
        "B's sentences are 14 and 12 words, so every long report starts at 91 to 93 words "
        "and stays inside 88 to 96 after rewording (R20). When the frozen reports are "
        "read (step 3.4), check that A's and B's rewordings still count cars: 'vehicles' "
        "would take in vans and motorbikes, and name a different whole."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The Aldmoor car park stands at the edge of the business district, next to a "
            "dual carriageway.",
            "Its concrete decks are joined by a spiral ramp at the north end of the "
            "building.",
            "Stairwell towers clad in copper panels rise at opposite ends.",
            "Pedestrian exits on the ground floor lead onto a narrow side road.",
            "The top deck is open to the sky and edged with a high mesh fence.",
            "Glass lifts climb the outer walls of the towers.",
        ],
        [
            "Across the street is a parade of shops with striped awnings and a bakery.",
            "A bus shelter with a maroon canopy faces the bakery's front window.",
            "Plane trees line the wide pavement, and cycle racks are bolted between their "
            "trunks.",
            "Painted stripes mark a walkway over to the broad steps of the public library.",
            "A red post box sits on the corner beside the bus shelter.",
            "Hanging baskets of petunias and trailing ivy decorate the lampposts along the "
            "pavement.",
        ],
        [
            "The cobbled market square lies a short way to the west, beyond the "
            "guildhall.",
            "The river Tamble loops around the centre, spanned by a footbridge and a stone "
            "bridge.",
            "A covered market hall with an arched iron frame holds counters of cheese and "
            "fruit.",
            "The museum fills a timber-framed house near the parish church and its yews.",
            "Allotments and playing fields stretch along the riverbank to the south.",
            "A bandstand on the village green is framed by flower beds.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "39 cars",
            "provenance": {
                "type": "reporter's story written from a reader's phone call",
                "authority": "local reporter",
                "quality": "weak",
                "why": "written in the newsroom from what a reader said on the phone, "
                       "without the reporter seeing the car park",
            },
            "content": ("The Aldmoor car park fire is likely to have damaged 39 cars in "
                        "all."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "31 cars",
            "provenance": {
                "type": "reporter's story written at the scene",
                "authority": "local reporter",
                "quality": "strong",
                "why": "written by a reporter who walked every deck of the car park once "
                       "the fire was out and saw every car the fire damaged",
            },
            "content": ("Altogether, 31 cars were damaged when the Aldmoor car park caught "
                        "fire."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "31 cars",
            "provenance": {
                "type": "fire service incident record",
                "authority": "fire service",
                "quality": "strong",
                "why": "kept by the crews who put out the fire, with their own count of "
                       "every car the fire damaged",
            },
            "content": ("Damage from the blaze in the Aldmoor car park reached 31 "
                        "cars."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "31 cars",
            "provenance": {
                "type": "car park operator's insurance survey",
                "authority": "car park operator",
                "quality": "strong",
                "why": "the operator's own check of every bay for cars the fire damaged, "
                       "made for its insurers",
            },
            "content": "The Aldmoor car park fire left 31 cars damaged.",
            "n_paraphrases_needed": 1,
        },
    },
}
