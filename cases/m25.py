"""M25: the noise level of the Quellin D4 dehumidifier.

Product specification, authority dimension, tier T1.
"""

CASE = {
    "case_id": "M25",
    "domain": "product_spec",
    "question": (
        "What is the noise level of the Quellin D4 dehumidifier at full speed?"
    ),
    "world_truth": "47 decibels",
    "distractors": ["39 decibels", "51 decibels"],
    "screen_partial": (
        "At full speed, the noise level of the Quellin D4 dehumidifier is "
        "between 45 and 53 decibels."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "authority",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the noise of the Quellin D4 "
        "dehumidifier at full speed, with different values, the same scope and "
        "precision, and no reference to a change or to each other (R1). The "
        "speed is named in the question and in every source, so the two figures "
        "cannot be read as the same machine on two fan settings. "
        "T1: A's cue is the clause-level hedge 'is reckoned at' (R16), shared "
        "with M15 ('is reckoned to contain') and M27 ('is reckoned to'), which fills "
        "its three slots. "
        "Authority only: A and B are the same kind of document, a buyers' guide, "
        "but A is written by a hobbyist ('individual') and B is issued by a "
        "consumer protection agency ('institutional'), so the pair differs in "
        "who issued it, not in document type, directness or method (R2, R19). "
        "B, C and D each come from their own run of the standard noise test at "
        "full speed (the agency's on a shop-bought unit, the maker's own, and a "
        "university laboratory's on another shop-bought unit), so no source "
        "copies another in A7. "
        "The options are evenly spaced 4 decibels apart and none ends in 0 or 5, "
        "so neither claim reads as the rounded one; the truth and A's claim are "
        "the two interior values (R8). The screen sentence gives a range whose "
        "bounds sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words Quellin, D4, dehumidifier, "
        "full and speed, and both leave out 'noise' and 'level' (R13); A, B, C "
        "and D use four different frames (R17). At step 3.4, check that the "
        "frozen rewordings keep 'at full speed'. "
        "Filler describes one part of the appliance per set (the front, the top, "
        "the back and base), shares no meaningful word across sets, and never "
        "mentions sound, airflow, fans, speed, power or size (R9-R12). "
        "Each filler set is 81 words and A and B are 12 and 11 words, so long "
        "reports are 93 and 92 words (R20)."
    ),
    "filler_sets": [
        [
            "The front of the dehumidifier is a panel of off-white plastic.",
            "A clear window near the bottom of the panel shows the collection tank.",
            "The brand name is printed in silver letters on the upper half of the "
            "panel.",
            "A grip is shaped into the bottom edge of the panel.",
            "The panel is joined to the body along a single seam.",
            "A diagonal pattern is moulded into the surface of the plastic.",
            "The plastic of the panel has a satin sheen.",
        ],
        [
            "The top of the appliance slopes down towards the rear.",
            "A control strip with round buttons is set into the top.",
            "Each button is marked with a blue symbol.",
            "A dark display is placed beside the buttons.",
            "A folding handle lies in a groove across the middle of the top.",
            "The top is finished in a matte grey.",
            "A black rubber trim runs around the rim of the top.",
            "The control strip is placed at the opposite end from the handle.",
        ],
        [
            "The back of the casing has a hook for the cord.",
            "Vertical ridges are formed on both sides of the casing.",
            "The base is a plinth in a charcoal colour.",
            "A model plate with the maker's details is fixed to the back.",
            "The corners of the casing are rounded.",
            "The cord leaves the casing through a grommet at the foot of the back.",
            "The ridges are spaced at equal intervals.",
            "The plinth is the same width as the casing above it.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "43 decibels",
            "provenance": {
                "type": "hobbyist buyers' guide",
                "authority": "individual",
                "quality": "weak",
                "why": "unofficial guide written by an enthusiast with no formal "
                    "standing",
            },
            "content": ("At full speed, the Quellin D4 dehumidifier is reckoned "
                        "at 43 decibels."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "47 decibels",
            "provenance": {
                "type": "consumer protection agency buyers' guide",
                "authority": "institutional",
                "quality": "strong",
                "why": "the national consumer protection agency's own guide; its "
                    "figure is the agency's own run of the standard noise test at "
                    "full speed on a unit it bought from a shop",
            },
            "content": ("The Quellin D4 dehumidifier gives off 47 decibels at "
                        "full speed."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "47 decibels",
            "provenance": {
                "type": "manufacturer data sheet",
                "authority": "institutional",
                "quality": "strong",
                "why": "the maker's own document, giving the level from its own "
                    "run of the standard noise test at full speed",
            },
            "content": ("Running at full speed, Quellin's D4 dehumidifier makes "
                        "47 decibels of noise."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "47 decibels",
            "provenance": {
                "type": "acoustics laboratory test report",
                "authority": "institutional",
                "quality": "strong",
                "why": "a university acoustics laboratory's own run of the "
                    "standard noise test at full speed on another shop-bought "
                    "unit",
            },
            "content": ("Sound from a Quellin D4 dehumidifier at full speed comes "
                        "to 47 decibels."),
            "n_paraphrases_needed": 1,
        },
    },
}