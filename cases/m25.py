"""M25: the noise level of the Quellin D4 dehumidifier.

Product specification, authority dimension, tier T1.
"""

CASE = {
    "case_id": "M25",
    "domain": "product_spec",
    "question": "What is the noise level of the Quellin D4 dehumidifier?",
    "world_truth": "45 decibels",
    "distractors": ["35 decibels", "50 decibels"],
    "screen_partial": (
        "The noise level of the Quellin D4 dehumidifier is between 43 and 52 "
        "decibels."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "authority",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about the noise of the Quellin D4 "
        "dehumidifier, with different values, the same scope and precision, and "
        "no reference to a change or to each other (R1). "
        "T1: A's cue is the hedge 'may be' (R16), not used by any other case. "
        "Authority only: A and B are the same kind of document, a buyers' guide, "
        "but A is written by a hobbyist ('individual') and B is issued by a "
        "consumer standards board ('institutional'), so the pair differs in who "
        "issued it, not in document type, directness or method (R2, R19). B, C "
        "and D all give the rated noise level at the standard setting, so the "
        "three agreeing sources state the same figure in A7. "
        "The options are evenly spaced, with the truth and A's claim as the two "
        "interior values (R8). The screen sentence gives a range whose bounds "
        "sit equally far from the two options it keeps (R15). "
        "A and B share exactly the question words noise, Quellin, D4 and "
        "dehumidifier, and both leave out 'level' (R13); A, B, C and D use four "
        "different frames (R17). "
        "Filler describes one part of the appliance per set (the front, the top, "
        "the back and base), shares no meaningful word across sets, and never "
        "mentions sound, airflow, fans, power or size (R9-R12). "
        "Each filler set is 81 words and A and B are 11 and 10 words, so long "
        "reports are 92 and 91 words (R20)."
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
            "claim": "40 decibels",
            "provenance": {
                "type": "hobbyist buyers' guide",
                "authority": "individual",
                "quality": "weak",
                "why": "unofficial guide written by an enthusiast with no formal "
                    "standing",
            },
            "content": ("The noise of the Quellin D4 dehumidifier may be "
                        "40 decibels."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "45 decibels",
            "provenance": {
                "type": "consumer standards board buyers' guide",
                "authority": "institutional",
                "quality": "strong",
                "why": "official guide giving the board's own certified rating "
                    "of the noise level at the standard setting",
            },
            "content": ("The Quellin D4 dehumidifier gives off 45 decibels "
                        "of noise."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "45 decibels",
            "provenance": {
                "type": "manufacturer data sheet",
                "authority": "institutional",
                "quality": "strong",
                "why": "the maker's rated noise level at the standard setting",
            },
            "content": ("Quellin rates the D4 dehumidifier's noise "
                        "at 45 decibels."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "45 decibels",
            "provenance": {
                "type": "acoustic laboratory certificate",
                "authority": "institutional",
                "quality": "strong",
                "why": "a separate laboratory confirmed the rated noise level "
                    "at the standard setting",
            },
            "content": ("Sound from a Quellin D4 dehumidifier comes to "
                        "45 decibels."),
            "n_paraphrases_needed": 1,
        },
    },
}