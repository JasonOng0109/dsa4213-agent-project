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
        "and maker (R13). The T1 cue is A's clause-level hedge 'is estimated to be' (R16). Quality resides "
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
        "are A=14 and B=13 words (|A - B| <= 2). Each filler set is 78 words, landing every long report "
        "at 91 or 92 words within the tight 91-93 band (R20). Fillers describe neutral physical aspects "
        "of the machine without cross-set noun repetition (R12), containing no numbers, measurements, time markers, or "
        "coffee brewing vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "The HydroBrew C8 coffee maker has a matte black housing with rounded corners and a finish.",
            "A silver strip runs beneath the upper rim beside a circular indicator with a dark centre.",
            "The side panels slope toward a platform with a charcoal finish and clean joins.",
            "Rubber feet support the appliance above a flat surface without visible gaps or loose edges.",
            "A small metal emblem sits near the front face beside a recessed handle with a curved outline.",
        ],
        [
            "A removable tray has a grey surface and a lip around its rim, with rounded corners.",
            "A perforated metal grille sits beside a recess below the front fascia and a display.",
            "Rounded plastic corners meet a dark side frame beneath a rectangular display with a clear cover.",
            "A back plate has raised strips and recessed screw heads beside a horizontal seam.",
            "Catches sit below the lower rim beside a curved cover with a satin finish and plain surface.",
        ],
        [
            "A power cord leaves the back through a round rubber opening set below the appliance.",
            "A shallow channel runs beneath the underside beside rectangular clips and a recessed groove.",
            "A square rocker switch sits near the lower border beside a smooth plastic surround with curved corners.",
            "The back shell has narrow ventilation slots arranged beneath a broad horizontal seam and smooth lip.",
            "Raised strips cross the underside between the supports and the back, leaving a clear central space.",
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