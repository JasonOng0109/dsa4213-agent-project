"""M33: how many homes the landslip at Harnwick Hill damaged.

Incident or status reports, authority dimension, tier T2. A and B are equally flat
statements with no cue in the content, so only provenance can tell them apart.
"""

CASE = {
    "case_id": "M33",
    "domain": "incident_status",
    "question": "How many homes were damaged by the landslip at Harnwick Hill?",
    "world_truth": "11 homes",
    "distractors": ["7 homes", "13 homes"],   # plausible, unsupported, same kind as
                                              # the truth; even steps of 2 homes
    "screen_partial": (
        "Between 8 and 12 homes were damaged by the landslip at Harnwick Hill."
    ),   # screen level P1: true, keeps 9 and 11 homes, each 1 home inside a bound, and
         # rules out 7 and 13 homes
    "quality_dimension": "authority",
    "difficulty_tier": "T2",            # no cue by design: A and B are equally flat,
                                        # so nothing in the content can be lost
    "design_notes": (
        "A and B state the same proposition, how many homes the landslip at Harnwick "
        "Hill damaged, with different values, in one sentence each. Both tie the count "
        "to the landslip, not to the hill, so neither counts only the homes on the hill "
        "while the other counts every home the landslip reached; both count whole homes "
        "and refer to no change and to no other source (R1). Read without provenance, "
        "neither is narrower, an exception to the other, or more precise. The case is "
        "T2 by design: the content carries no cue at all, no hedge and no difference in "
        "register, so A and B read as equally confident and only provenance can "
        "separate them. For a T2 case the outcome to read is belief, not accuracy "
        "('Tiers'). The quality dimension, authority, lives in provenance: both type "
        "names are statements, so the kind of document is the same, and they differ "
        "only in who stands behind them, an informal volunteer group against the fire "
        "and rescue service that led the response (R19). Neither name says how its "
        "figure was found, how close its writer was or that it copies another, and "
        "neither suggests a stake in the figure, as a residents' group would; neither "
        "says 'independent', and both name the source rather than the subject, so no "
        "word a rewording needs is banned (R2a). The options are 7, 9, 11 and 13 homes, "
        "evenly spaced, so the truth and A's claim are both interior and equally close "
        "to the average: neither 'avoid the extremes' nor 'pick the middle' finds the "
        "truth (R8). None is a round figure, and A's claim is the lower one, so neither "
        "a habit for round numbers nor a belief that unofficial figures run high finds "
        "the truth; in most cases written so far, A's claim is the higher figure. The "
        "options carry their unit, as the content does, so an answer that copies 'homes' "
        "still matches an option. The screen sentence keeps 9 and 11, each 1 home "
        "inside a bound, so 'pick the survivor nearest the bound' does not find the "
        "truth (R15). A and B use every question word except 'many' (R13). B, C and D "
        "state the fact in three different frames (R17). B's crews checked each home "
        "in the path of the slip, and C and D are separate counts of the same homes, "
        "the district council's building control record and a local newspaper report, "
        "so none of the three depends on another, and no sentence says how its value "
        "was found (R2, R6). All three count every home the landslip damaged, so B, C "
        "and D support one proposition in A7 (R1). The hill, the landslip and the "
        "damage are invented (R4). Filler describes the hill and its footpath in set 1, "
        "the shops at the bottom of the lane in set 2, and the park by the river in set "
        "3, with nothing about homes, damage, the ground, weather, clearing up or the "
        "emergency, no figures and no second person, so no slot carries the feel of "
        "either source (R3, R9, R10). No distinctive word is in more than one set, so "
        "the slots stay apart (R12). Each filler set is 83 words and A's and B's "
        "sentences are 8 and 10 words, so every long report starts at 91 to 93 words "
        "and stays inside 88 to 96 after rewording (R20). When the frozen reports are "
        "read (step 3.4), check that A's and B's rewordings still count homes damaged "
        "by the landslip: 'destroyed' or 'evacuated' would change the measure, "
        "'properties' or 'buildings' the unit, since they could take in the shops of "
        "set 2, and 'homes on the hill' would narrow the place."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # the hill and its footpath
            "Harnwick Hill rises above the valley, with a footpath winding up to its "
            "grassy top.",
            "A wooden bench near the summit faces the distant blue moors.",
            "Gorse bushes flower bright yellow along both sides of the footpath.",
            "A stone pillar at the highest point is carved with the names of nearby "
            "peaks.",
            "Skylarks nest in the long grass, and their song carries across the open top.",
            "A low drystone wall bounds the edge of the summit.",
            "Kestrels often hover high above the hill.",
        ],
        [   # the shops at the bottom of the lane
            "A short parade of shops sits at the bottom of the lane.",
            "The bakery sells warm rolls, iced buns and thick slices of fruit cake.",
            "Next door, a hardware store stacks clay plant pots by its entrance.",
            "A chemist with a green cross sign stands on the corner.",
            "The cafe has tables under a striped awning and a chalkboard menu.",
            "A red post box and a bus shelter stand together near the kerb.",
            "Hanging baskets of deep pink petunias decorate the shop fronts.",
        ],
        [   # the park by the river
            "Beside the river, a public park has a playground with swings and a slide.",
            "A painted bandstand occupies the middle of a wide lawn.",
            "Ducks and moorhens paddle near a footbridge that spans the water.",
            "Willow trees lean over the riverbank, their branches trailing in the stream.",
            "A cricket pitch at the far end is marked out with white lines.",
            "Allotment plots beyond the pitch grow beans, onions and sunflowers.",
            "A little kiosk by the gates offers ice creams and mugs of tea.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "9 homes",
            "provenance": {
                "type": "volunteer group statement",
                "authority": "informal",
                "quality": "weak",
                "why": "an informal volunteer group with no official role in the "
                       "emergency response or in assessing the damage",
            },
            "content": "The landslip at Harnwick Hill damaged 9 homes.",
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "11 homes",
            "provenance": {
                "type": "fire and rescue service statement",
                "authority": "institutional",
                "quality": "strong",
                "why": "issued by the fire and rescue service, which led the emergency "
                       "response on the hill; its crews checked each home in the path "
                       "of the slip",
            },
            "content": "In the landslip at Harnwick Hill, 11 homes were damaged.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "11 homes",
            "provenance": {
                "type": "council building control record",
                "authority": "institutional",
                "quality": "strong",
                "why": "building control officers from the district council inspected "
                       "every home near the landslip and listed each damaged one",
            },
            "content": "The Harnwick Hill landslip left 11 homes damaged.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "11 homes",
            "provenance": {
                "type": "local newspaper report",
                "authority": "press",
                "quality": "strong",
                "why": "a reporter walked every street around the landslip and counted "
                       "each damaged home",
            },
            "content": "Damage from the landslip on Harnwick Hill reached 11 homes.",
            "n_paraphrases_needed": 1,
        },
    },
}
