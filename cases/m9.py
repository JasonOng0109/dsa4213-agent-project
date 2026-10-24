"""M9: Weight of the fictional NoriSound S5 Bluetooth speaker.

Product specifications domain, directness quality dimension, tier T2.
Tests conflicting speaker weights reported through firsthand
and secondhand observations.
"""

CASE = {
    "case_id": "M9",
    "domain": "product_spec",
    "question": (
        "What is the weight of the NoriSound S5 Bluetooth speaker, "
        "excluding its packaging?"
    ),
    "world_truth": "810 g",
    "distractors": ["570 g", "930 g"],
    "screen_partial": (
        "The NoriSound S5 Bluetooth speaker weighs more than 650 g "
        "and less than 850 g without its packaging."
    ),
    "quality_dimension": "directness",
    "difficulty_tier": "T2",
    "design_notes": (
        "M9 tests the directness quality dimension using conflicting "
        "weight claims for the fictional NoriSound S5 Bluetooth speaker. "
        "Source A reports 690 g, while Source B supports the true value "
        "of 810 g. Both concern the same speaker model without packaging "
        "or accessories, with equally specific claims and no exceptions "
        "or changes (R1). "
        "The case is T2 because A and B are equally confident statements "
        "without uncertainty hedges or measurement-method cues in content. "
        "Their quality difference is carried by provenance. "
        "Source A is a relayed account from product-handling staff, "
        "whereas Source B is an eyewitness account from equally ranked "
        "staff. Both have matching authority and refer to weighings "
        "using calibrated scales, isolating directness rather than "
        "authority or method (R19). "
        "Source identities and weighing procedures remain in provenance "
        "rather than content (R2). A and B describe the same weight "
        "property with no substantive question-wording advantage (R13). "
        "Sources B, C and D support 810 g using distinct sentence frames "
        "(R17). C and D refer to separate physical units weighed using "
        "different calibrated scales, with D's observation taking place "
        "at another site. Their separate origins reduce dependence "
        "between the three strong sources (R6, A7). "
        "The four options are 570, 690, 810 and 930 g, with the competing "
        "claims occupying the interior positions and avoiding round "
        "hundreds (R8). The screening sentence retains 690 and 810 g "
        "while excluding 570 and 930 g (R15). "
        "The three filler sets describe different parts of the speaker: "
        "front grille, top controls, and base and rear casing. "
        "They avoid weight information, packaging specifications, "
        "measurement procedures and firsthand handling clues, "
        "while using distinct vocabulary (R9, R10, R12). "
        "Filler and source lengths are checked against R20. "
        "M9 is the backup for M22 in the ten-case subset."
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The NoriSound S5 speaker has a woven fabric grille covering its curved front surface.",
            "The fabric has a fine crosshatched weave of charcoal and pale grey threads.",
            "A stitched logo sits low on the grille in a paler shade of grey.",
            "A neat seam traces the line where the grille meets the shell.",
            "The shell has a plain matte finish in a matching dark tone.",
            "Its corners curve gently, which gives the front a soft and rounded outline.",
        ],
        [
            "Control buttons are set in a recessed strip across the top of the device.",
            "Each button bears a simple icon printed in crisp white ink.",
            "A tiny status lamp is placed beside the buttons, at the far end of the strip.",
            "The strip is glossy black, in clear contrast to the body around it.",
            "A thin glossy trim borders the strip on every side.",
            "The buttons stand almost flush with the strip, so the top is level and tidy.",
        ],
        [
            "A flat base keeps the casing upright on a desk, a shelf or a windowsill.",
            "A rubber lip circles the casing just above the base.",
            "The rear panel is moulded with a faint ribbed texture from edge to edge.",
            "The ribs form close parallel ridges, much like those on corduroy trousers.",
            "A slim groove runs vertically down the middle of the panel, dividing the ribs.",
            "The model name is embossed beside the groove in small, square capital letters.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "690 g",
            "provenance": {
                "type": "relayed account from product-handling staff",
                "authority": "product-handling staff",
                "quality": "weak",
                "why": (
                    "The staff member was not present when the speaker "
                    "was weighed on a calibrated scale, unpackaged and "
                    "without accessories, and repeats the figure a "
                    "colleague passed on, so a slip in passing it on "
                    "carries over."
                ),
            },
            "content": (
                "The NoriSound S5 Bluetooth speaker has a weight "
                "of 690 g without packaging."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "810 g",
            "provenance": {
                "type": "eyewitness account from product-handling staff",
                "authority": "product-handling staff",
                "quality": "strong",
                "why": (
                    "The staff member personally witnessed the speaker "
                    "being weighed without packaging or accessories "
                    "using a calibrated scale."
                ),
            },
            "content": (
                "For the NoriSound S5 Bluetooth speaker without packaging, "
                "the weight is 810 g."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "810 g",
            "provenance": {
                "type": "separate firsthand observation",
                "authority": "product-handling staff",
                "quality": "strong",
                "why": (
                    "A second staff member watched a different unit "
                    "being weighed, unpackaged and without accessories, "
                    "on a different calibrated scale."
                ),
            },
            "content": (
                "The unpackaged NoriSound S5 Bluetooth speaker "
                "has a weight of 810 g."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "810 g",
            "provenance": {
                "type": "another firsthand observation",
                "authority": "product-handling staff",
                "quality": "strong",
                "why": (
                    "A third staff member, at another site, watched "
                    "a third unit being weighed, unpackaged and without "
                    "accessories, on that site's own calibrated scale."
                ),
            },
            "content": (
                "The NoriSound S5 Bluetooth speaker, without packaging, "
                "weighs 810 g."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}