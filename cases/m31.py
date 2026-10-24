"""M31: the noise level of the Ostvale Arcline dishwasher.

Product specifications domain, primary-source dimension, tier T2. A and B are equally flat
statements with no cue in the content, so only provenance can tell them apart.
"""

CASE = {
    "case_id": "M31",
    "domain": "product_spec",
    "question": "What is the noise level of the Ostvale Arcline dishwasher?",
    "world_truth": "44 dB",
    "distractors": ["40 dB", "52 dB"],   # plausible, unsupported, same kind as the
                                         # truth; even steps of 4 dB
    "screen_partial": (
        "The Ostvale Arcline dishwasher has a noise level between 42 and 50 dB."
    ),   # screen level P1: true, keeps 44 and 48 dB, each 2 dB inside a bound, and
         # rules out 40 and 52 dB
    "quality_dimension": "primary_source",
    "difficulty_tier": "T2",            # no cue by design: A and B are equally flat,
                                        # so nothing in the content can be lost
    "design_notes": (
        "A and B state the same proposition, the noise level of the Ostvale Arcline "
        "dishwasher, with different values, in one sentence each. Both name the same "
        "machine, give whole decibels in the same unit, and refer to no change and to no "
        "other source (R1). Read without provenance, neither is narrower, an exception "
        "to the other, or more precise. The case is T2 by design: the content carries no "
        "cue at all, no hedge and no difference in register, so A and B read as equally "
        "confident and only provenance can separate them. For a T2 case the outcome to "
        "read is belief, not accuracy ('Tiers'). The quality dimension, primary source, "
        "lives in provenance: both type names are the manufacturer's own, so the writer's "
        "standing is the same, and they differ only in the document, a listing in its "
        "online shop, which copies its details from the maker's documents, against the "
        "technical datasheet itself (R19). Neither says 'independent', and both name the "
        "source rather than the "
        "subject, so no word a rewording needs is banned (R2a). The options are 40, 44, "
        "48 and 52 dB, evenly spaced, so the truth and A's claim are both interior and "
        "equally close to the average: neither 'avoid the extremes' nor 'pick the "
        "middle' finds the truth (R8). The steps are 4 dB rather than 2, so the two "
        "claims cannot be read as one machine heard on different wash programmes or "
        "measured twice, and all four are ordinary figures for a dishwasher. The screen "
        "sentence keeps 44 and 48 dB, each 2 dB inside a bound, so 'pick the survivor "
        "nearest the bound' does not find the truth (R15). A, B and D use every question "
        "word (R13); C leaves out 'level', which the linter only notes, since B, C and D "
        "always appear together. B, C and D state the fact in three different frames "
        "(R17). C and D are tests of units bought from shops, by a consumer association "
        "and by a market surveillance inspector, so neither depends on the "
        "manufacturer's datasheet or on each other, and neither's sentence says how its "
        "value was found (R2, R6). Their whys tie them to the test behind B's figure: "
        "the datasheet gives the noise level from the standard noise test, and both "
        "tests were run to it, so B, C and D support one proposition in A7, not a "
        "rating against two different measurements (R1). The brand, the model and its "
        "noise level are invented (R4). Filler describes one part of the machine per "
        "set, the baskets in set 1, the door and its controls in set 2, and the outer "
        "casing and plinth in set 3, so no content word is in two sets and "
        "the slots stay apart (R12). It says nothing about noise, wash programmes, "
        "installation, testing, shops or documents, and has no figures and no second "
        "person, so no slot carries the feel of either source (R3, R9, R10). Each "
        "filler set is 82 words and A's and B's "
        "sentences are 10 and 11 words, so every long report starts at 92 or 93 words "
        "and stays inside 88 to 96 after rewording (R20)."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # the baskets
            "The Ostvale Arcline dishwasher has a lower basket for plates and pans and an "
            "upper basket for cups and glasses.",
            "A slim cutlery tray slides out on runners above the upper basket.",
            "Folding tines in the lower basket lie flat to make room for larger pots.",
            "A narrow fold-down shelf at one end of the upper basket holds small cups.",
            "Spray arms turn on a hub beneath each basket.",
            "The wire baskets have a smooth white plastic coating that wipes clean easily.",
        ],
        [   # the door and its controls
            "The door opens downwards on firm hinges and rests open at almost any angle.",
            "Its handle is a recessed bar that runs across the full width of the door.",
            "Touch buttons sit in a neat line along the rim of the door.",
            "The detergent dispenser sits on the inside of the door, beside a rinse-aid "
            "cap.",
            "A soft rubber seal runs around the inner edge of the door.",
            "A tiny green light beside the buttons glows when the child lock is on.",
        ],
        [   # the outer casing and plinth
            "The top of the machine is a solid panel of brushed steel with rounded corners.",
            "A black plinth along the bottom hides the feet and the hoses behind it.",
            "The side panels are finished in the same brushed steel as the top.",
            "A thin strip of grey trim frames the whole front face of the casing.",
            "The back panel is plain metal, with a slotted vent near the base.",
            "Short feet at each corner keep the casing just clear of the floor.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "48 dB",
            "provenance": {
                "type": "manufacturer's online shop listing",
                "authority": "manufacturer",
                "quality": "weak",
                "why": "the maker's sales page for this machine, with details copied from "
                       "its technical documents, so a slip in the copying carries over",
            },
            "content": "The Ostvale Arcline dishwasher has a 48 dB noise level.",
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "44 dB",
            "provenance": {
                "type": "manufacturer's technical datasheet",
                "authority": "manufacturer",
                "quality": "strong",
                "why": "the maker's own document for this machine, giving the noise level "
                       "from the standard noise test, and the original that every "
                       "listing copies",
            },
            "content": "The Ostvale Arcline dishwasher produces a noise level of 44 dB.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "44 dB",
            "provenance": {
                "type": "consumer association test report",
                "authority": "consumer group",
                "quality": "strong",
                "why": "a consumer group's test of a unit bought from a shop, run to the "
                       "standard noise test",
            },
            "content": "The Ostvale Arcline dishwasher makes forty-four decibels of noise.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "44 dB",
            "provenance": {
                "type": "market surveillance inspection record",
                "authority": "regulator",
                "quality": "strong",
                "why": "a product regulator's check of another shop-bought unit, using the "
                       "same standard test",
            },
            "content": "Ostvale's Arcline dishwasher runs at a 44 dB noise level.",
            "n_paraphrases_needed": 1,
        },
    },
}
