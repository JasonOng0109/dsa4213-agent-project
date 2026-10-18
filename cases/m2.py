"""M2: Battery capacity of the fictional Arden Air 14 laptop.

Product specifications, primary-source quality dimension, tier T1.
Tests conflicting battery specifications from a retailer and manufacturer.
"""

CASE = {
    "case_id": "M2",
    "domain": "product_spec",
    "question": "What is the battery capacity of the Arden Air 14 laptop?",
    "world_truth": "65 Wh",
    "screen_partial": (
        "The Arden Air 14 laptop has a battery capacity "
        "greater than 50 Wh and less than 70 Wh."
    ),
    "distractors": ["45 Wh", "75 Wh"],
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",
    "design_notes": (
        "This case tests primary-source quality using conflicting battery capacities "
        "for the fictional Arden Air 14 laptop. Source A is a third-party retailer "
        "listing that incorrectly claims 55 Wh, while Source B is the manufacturer's "
        "specification sheet supporting the true value of 65 Wh. "
        "A and B describe the same battery capacity with equally specific claims "
        "and no changes or exceptions (R1). Both use the same relevant question "
        "words, so the question does not favour either claim (R13). "
        "Source A contains the mild clause-level hedge 'is understood to have', "
        "which is intended to survive paraphrasing (R16). The T1 classification "
        "will be checked against the frozen reports and changed to T2 if the "
        "hedge disappears. "
        "Source identity, reliability and evidence-production methods are kept "
        "in provenance rather than content (R2). Sources B, C and D use distinct "
        "sentence structures while supporting the same true value (R17). "
        "Their independent origins are recorded in provenance for A7. "
        "The four options are 45, 55, 65 and 75 Wh, with both competing claims "
        "as interior values (R8). The screen sentence keeps 55 and 65 Wh while "
        "excluding 45 and 75 Wh, preserving the world truth (R15). "
        "The three filler sets describe only neutral physical features of the "
        "laptop, without battery-related information or source-identifying "
        "language (R9, R10). Each filler set contains 78 words; A and B contain "
        "15 and 14 words respectively, producing long reports of 93 and 92 "
        "words before paraphrasing (R20)."
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The Arden Air 14 laptop has a smooth lid with a small emblem positioned "
            "near its centre.",
            "Its keyboard uses rounded keys arranged in an even layout across "
            "the upper deck.",
            "A broad touchpad sits below the keyboard, with a matte surface that "
            "feels smooth to the touch.",
            "The screen is surrounded by a narrow border with a webcam above "
            "the display.",
            "Speaker openings sit beside the keyboard, while the hinge allows "
            "the lid to tilt back smoothly.",
        ],
        [
            "The Arden Air 14 laptop has a textured underside with small rubber "
            "feet at the corners.",
            "The hinge connects the display to the main body and moves smoothly "
            "through its range.",
            "A shallow recess near the front edge makes the lid easier to lift "
            "without much effort.",
            "The keyboard deck has a plain finish, and the touchpad is centred "
            "beneath the keys.",
            "The webcam sits above the screen, with a tiny opening beside its "
            "lens for the microphone.",
        ],
        [
            "The Arden Air 14 laptop has a compact keyboard with a clearly "
            "marked space bar.",
            "The display frame has a uniform finish, and its corners are gently "
            "rounded along the outer edges.",
            "Small speaker grilles appear along the sides of the keyboard deck, "
            "beside the keys.",
            "The touchpad has a smooth surface with no visible separate buttons "
            "on its face.",
            "The lid closes flush against the base, and the hinge is mostly "
            "hidden when the laptop is open.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "55 Wh",
            "content": (
                "The Arden Air 14 laptop is understood to have "
                "a battery capacity of 55 Wh."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "online retailer product listing",
                "authority": "Third-party retailer",
                "quality": "weak",
                "why": (
                    "The retailer reproduces specifications "
                    "but does not originate the product information."
                ),
            },
        },
        "B": {
            "quality": "strong",
            "claim": "65 Wh",
            "content": (
                "The battery in the Arden Air 14 laptop "
                "has a capacity of 65 Wh."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "manufacturer specification sheet",
                "authority": "Product manufacturer",
                "quality": "strong",
                "why": (
                    "The manufacturer directly establishes the "
                    "technical specifications of the laptop."
                ),
            },
        },
        "C": {
            "quality": "strong",
            "claim": "65 Wh",
            "content": (
                "Sixty-five watt-hours is the battery capacity "
                "of the Arden Air 14 laptop."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "accredited laboratory test report",
                "authority": "Independent testing laboratory",
                "quality": "strong",
                "why": (
                    "The laboratory independently verifies the "
                    "battery specification through technical testing."
                ),
            },
        },
        "D": {
            "quality": "strong",
            "claim": "65 Wh",
            "content": (
                "Inside the Arden Air 14 laptop "
                "sits a 65 Wh battery."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "product certification record",
                "authority": "Independent certification body",
                "quality": "strong",
                "why": (
                    "The certification body independently documents "
                    "the laptop battery specification."
                ),
            },
        },
    },
}
