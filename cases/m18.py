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
        "The hedge is used in M12, M18 and M20 (3 slots all filled). Quality resides "
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
        "of the machine as three separate feature groups with no repeated distinctive nouns across sets (R12), "
        "containing no numbers, measurements, time markers, or coffee brewing vocabulary (R3, R9, R10). "
    ),

    "filler_sets": [
        [
            "The HydroBrew C8 coffee maker has a matte black casing with rounded corners and charcoal finish.",
            "A narrow silver band runs beneath the top lid along its front edge near the hinge.",
            "The upper cover slopes gently toward a broad crown with a charcoal surface and shallow profile.",
            "A circular indicator appears beside the lid hinge on the rear portion of the cover.",
            "A small emblem is fixed near the upper rim above the front panel of casing.",
        ],
        [
            "A rectangular display is set into the front panel above several small front controls.",
            "A perforated grille spans the upper fascia beneath the display on the front panel near the top.",
            "Two narrow buttons sit beside a small circular indicator on the front face of casing.",
            "A smooth front border surrounds the controls and joins the side casing along its lower edge.",
            "A curved handle projects from the lower front edge beneath the control panel near the base.",
        ],
        [
            "A black power cord leaves the rear through a round rubber grommet near the lower rear base.",
            "Four short feet lift the base above the supporting surface on a low frame below.",
            "A square rocker switch is mounted beside the rear cable outlet on the lower rear casing.",
            "Narrow vents run across the underside between the rear supports along a flat underside panel.",
            "A broad base plate covers the lower frame beneath the appliance with a plain edge.",
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