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
    "world_truth": "800 g",
    "distractors": ["600 g", "900 g"],
    "screen_partial": (
        "The NoriSound S5 Bluetooth speaker weighs more than 650 g "
        "and less than 850 g without its packaging."
    ),
    "quality_dimension": "directness",
    "difficulty_tier": "T2",
    "design_notes": (
        "This case tests the directness quality dimension using conflicting "
        "weight claims for the fictional NoriSound S5 Bluetooth speaker. "
        "Source A reports 700 g, while Source B supports the true weight "
        "of 800 g. Both describe the same speaker without packaging or "
        "accessories, with equally specific claims and no exceptions or "
        "changes (R1). "
        "The case is T2 because A and B are equally confident statements "
        "with no uncertainty hedge or source-quality cue in their content. "
        "Their reliability difference is carried entirely by provenance. "
        "Source A is a secondhand account from product-handling staff who "
        "did not witness the weighing, whereas Source B is a firsthand "
        "account from staff who directly observed the weighing. Both have "
        "matching authority and refer to comparable calibrated weighing "
        "methods, isolating directness rather than authority or method (R19). "
        "Source identity and evidence-production details remain in provenance "
        "rather than content (R2). A and B identify the same product and "
        "weight property without a substantive difference in question-related "
        "wording (R13). "
        "Sources B, C and D support 800 g using distinct sentence structures "
        "(R17). C and D are based on separate firsthand weighings using "
        "comparable calibrated scales, rather than copying B's observation "
        "(R6, A7). Their independence and comparability depend on consistent "
        "speaker configuration, exclusion of accessories and weighing "
        "procedures, which should be checked during manual review. "
        "The four options are 600 g, 700 g, 800 g and 900 g, with the truth "
        "and A's incorrect claim occupying the two interior positions (R8). "
        "The screening sentence retains 700 g and 800 g while excluding "
        "600 g and 900 g, preserving the world truth (R15). "
        "The three filler sets describe distinct physical aspects of the "
        "speaker: its grille and exterior, decorative buttons and markings, "
        "and carrying loop and fittings. They contain no weight information, "
        "packaging specifications, measurement methods or source-identifying "
        "language, and use different vocabulary (R9, R10, R12). "
        "The filler and A/B sentence lengths satisfy the required long-report "
        "range, with no R20 warnings."
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The NoriSound S5 speaker has a woven fabric grille covering its curved front surface.",
            "A narrow seam follows the edge where the grille meets the surrounding outer shell.",
            "The fabric has a fine crosshatched texture with threads arranged in a regular pattern.",
            "Small rounded corners soften the outline, while the rear panel has a plain matte finish.",
            "A shallow decorative groove runs along the upper edge of the housing, ending near a small emblem pressed into the surface.",
        ],
        [
            "The speaker has rubber buttons arranged along a narrow strip near the upper surface.",
            "Each button has a raised symbol that can be felt easily beneath a fingertip.",
            "A small circular emblem sits beside the strip, surrounded by a recessed border.",
            "The surrounding material has a smooth satin texture with gently rounded transitions between the adjoining panels.",
            "Fine decorative markings appear along the rear edge, while a narrow band of contrasting material follows the lower contour of the enclosure.",
        ],
        [
            "The NoriSound S5 speaker includes a fabric carrying loop attached near the side of its housing.",
            "The loop passes through a reinforced opening with a smooth rounded border.",
            "A small metal clasp connects the fabric to an anchor hidden beneath the outer panel.",
            "The underside has rubber feet positioned near the corners to keep the enclosure steady on a surface.",            
            "A narrow trim piece follows the rear edge, with a subtle textured pattern continuing around the adjoining side.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "700 g",
            "provenance": {
                "type": "secondhand account from product-handling staff",
                "authority": "product-handling staff",
                "quality": "weak",
                "why": (
                    "The staff member received the weight information "
                    "from a colleague but did not witness the weighing. "
                    "The account refers to the unpackaged speaker "
                    "without accessories."
                ),
            },
            "content": (
                "The NoriSound S5 Bluetooth speaker has a weight "
                "of 700 g without its packaging."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "800 g",
            "provenance": {
                "type": "firsthand account from product-handling staff",
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
                "the measured weight is 800 g."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "800 g",
            "provenance": {
                "type": "separate firsthand weighing observation",
                "authority": "product-handling staff",
                "quality": "strong",
                "why": (
                    "Another staff member directly witnessed a separate "
                    "weighing of the same speaker configuration using "
                    "a comparable calibrated scale, independently of B."
                ),
            },
            "content": (
                "The unpackaged NoriSound S5 Bluetooth speaker "
                "has a weight of 800 g."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "800 g",
            "provenance": {
                "type": "another firsthand weighing observation",
                "authority": "product-handling staff",
                "quality": "strong",
                "why": (
                    "A third staff member directly observed an independent "
                    "weighing of the unpackaged speaker without accessories, "
                    "using a comparable calibrated scale."
                ),
            },
            "content": (
                "For the NoriSound S5 Bluetooth speaker, "
                "the weight without packaging is 800 g."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
