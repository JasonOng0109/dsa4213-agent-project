"""M18: Water tank capacity of the fictional HydroBrew C8 coffee maker.

Product specifications domain, primary-source quality dimension, tier T1.
"""

CASE = {
    "case_id": "M18",
    "domain": "product_spec",
    "question": "What is the water tank capacity of the HydroBrew C8 coffee maker?",
    "world_truth": "1440 ml",
    "distractors": ["680 ml", "1820 ml"],  # [680, 1060, 1440, 1820]
    "screen_partial": (
        "The water tank capacity of the HydroBrew C8 coffee maker is between 900 ml and 1600 ml."
    ),  # keeps 1060 and 1440 (truth); rules out 680 and 1820; both survivors sit 160 ml inside bounds (R15)
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",
    "design_notes": (
        "Primary-source dimension, T1. A and B state the same proposition (the water tank "
        "capacity of the HydroBrew C8 coffee maker) as single sentences with identical scope (R1). "
        "Both share the question content-words: water, tank, capacity, HydroBrew, C8, coffee, "
        "and maker (R13). The T1 cue is A's clause-level hedge 'is estimated to be' (R16). "
        "M12 and M20 have moved off 'estimated', so M18 is now its only case (R16). Quality resides "
        "strictly in provenance (R2, R19). Under Phase 4 primary-source rules, both writers share "
        "identical manufacturer standing ('maker product team'), isolating the primary-source dimension: "
        "A is the maker's online shop listing, while B is the maker's technical datasheet (R19). "
        "Neither type name leaks methodology, authority asymmetry, or the prohibited word 'independent' (R19). "
        "Sources B, C, and D state the truth using distinct syntactic frames to keep bigram overlap strictly "
        "below 0.40 (R17). B, C, and D each reach the figure by a separate route: B gives the maker's own "
        "capacity statement, C measures a shop-bought unit, and D measures another sample in a lab. Options "
        "form a balanced spread [680, 1060, 1440, 1820] ml, with the truth (1440) and A's claim (1060) "
        "occupying the interior positions (R8). The screen sentence uses two bounds (900 ml and 1600 ml), "
        "placing both survivors (1060 and 1440) exactly 160 ml inside the bounds (R15). Content lengths "
        "are A=14 and B=13 words (|A - B| <= 2). Filler sets are 78 or 79 words, landing every long "
        "report at 91 to 93 words within the tight 91-93 band (R20). Each filler set describes one part "
        "of the machine (the lid and top, the front panel and display, the base and cord) in plain "
        "one-fact sentences, so no feature appears in two slots and no content word is in two sets "
        "(R12). Filler has no numbers or number words, measurements, time markers, liquids or brewing "
        "vocabulary (R3, R9, R10). "
    ),

    "filler_sets": [
        [
            "The HydroBrew C8 coffee maker has a matte black casing with rounded corners.",
            "A hinged lid covers the top of the machine.",
            "A ridged grip runs along the lip of the lid.",
            "A narrow silver band trims the rim of the lid.",
            "The hinge is hidden beneath a smooth cover.",
            "The top surface has a soft satin finish in charcoal.",
            "A small engraved logo sits beside the hinge.",
            "The corners of the lid slope gently down to the casing.",
        ],
        [
            "A square display screen is set into the front panel.",
            "The screen shows crisp white symbols on a dark background.",
            "Square push buttons line up under the screen.",
            "Each button carries a printed icon in grey.",
            "A curved chrome handle stands out from the right side of the front panel.",
            "The front panel has a glossy coating in deep graphite.",
            "A thin chrome border frames the screen.",
            "The brand name is embossed above the screen in plain capitals.",
        ],
        [
            "The base is a wide, heavy plinth in brushed steel.",
            "Rubber feet keep the plinth steady on a kitchen counter.",
            "A braided power cord leaves the back of the base.",
            "The cord ends in a plug with a blue sleeve.",
            "A rocker switch is fitted at the rear of the plinth.",
            "Air vents form a fine mesh along the lower edge.",
            "A cable clip on the underside holds spare cord.",
            "The plinth has a neatly bevelled outline throughout.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "1060 ml",
            "content": (
                "The HydroBrew C8 coffee maker's water tank capacity is estimated to be 1060 ml."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "maker online shop listing",
                "authority": "maker product team",
                "quality": "weak",
                "why": "the maker's sales page for this machine, with details copied from its technical datasheet, so a slip in the copying carries over",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "1440 ml",
            "content": (
                "The HydroBrew C8 coffee maker has a water tank capacity of 1440 ml."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "maker technical datasheet",
                "authority": "maker product team",
                "quality": "strong",
                "why": "the maker's own document for this machine, giving the capacity as the water the tank holds filled to its MAX line, and the original the shop listing copies",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "1440 ml",
            "content": (
                "HydroBrew's C8 coffee maker holds 1440 ml in its water tank."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "consumer magazine product test",
                "authority": "consumer magazine",
                "quality": "strong",
                "why": "a consumer magazine's test of a unit bought from a shop, filling the tank to its MAX line and measuring the water it took",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "1440 ml",
            "content": (
                "The HydroBrew C8 coffee maker's tank has room for 1440 ml of water."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "certification lab test record",
                "authority": "certification lab",
                "quality": "strong",
                "why": "a certification lab's own test of another sample unit, filling the tank to its MAX line and measuring the water it took",
            },
        },
    },
}