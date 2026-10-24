"""M12: Key-travel distance of the fictional Velora K8 keyboard.

Product specifications domain, method dimension, tier T1.
Tests conflicting measurements obtained through different methods.
"""

CASE = {
    "case_id": "M12",
    "domain": "product_spec",
    "question": (
        "What is the key-travel distance of the Velora K8 "
        "wireless keyboard?"
    ),
    "world_truth": "2.0 mm",
    "distractors": ["1.6 mm", "2.2 mm"],
    "screen_partial": (
        "The key-travel distance of the Velora K8 wireless keyboard "
        "is greater than 1.7 mm and less than 2.1 mm."
    ),
    "quality_dimension": "method",
    "difficulty_tier": "T1",

    "design_notes": (
        "M12 tests the method quality dimension using conflicting "
        "key-travel measurements for the fictional Velora K8 wireless "
        "keyboard. Source A claims 1.8 mm while Source B supports "
        "the true value of 2.0 mm. Both describe the same key-travel "
        "distance for the same keyboard configuration, without "
        "exceptions or changes (R1). "
        "Source A uses a ruler-based displacement measurement, "
        "whereas B uses a calibrated displacement gauge. Both "
        "measurements are performed by product testing technicians "
        "with matching authority, isolating method quality (R19). "
        "Source A contains the mild hedge 'may well have', "
        "which is intended to survive faithful paraphrasing (R16); "
        "it names no method, which a method case's hedge must not. "
        "If the hedge disappears from frozen reports, the case "
        "will be relabelled T2. "
        "Source identities and measurement procedures remain "
        "in provenance rather than content (R2). "
        "A and B describe the same question-related property (R13). "
        "Sources B, C and D support 2.0 mm using different sentence "
        "structures (R17). C and D use separately operated "
        "calibrated displacement gauges and independently stored "
        "measurements rather than copying B's result (R6, A7). "
        "Their independence and measurement comparability require "
        "manual verification. "
        "The options 1.6, 1.8, 2.0 and 2.2 mm are evenly spaced, "
        "with the competing claims occupying interior positions "
        "(R8). The screening sentence retains 1.8 and 2.0 mm "
        "while excluding 1.6 and 2.2 mm (R15). "
        "The three filler sets describe distinct physical aspects "
        "of the keyboard without discussing key travel, measurement "
        "methods or source identity (R9, R10, R12). "
        "Filler and source lengths must be verified against R20."
    ),

    "filler_sets": [
        [
            "The Velora K8 keyboard has a rectangular frame with rounded corners and a plain finish.",
            "A narrow decorative border runs along the front edge of the housing.",
            "The upper surface has a consistent colour, with a small emblem near the corner.",
            "Fine seams separate the outer panels without exposing the internal fittings.",
            "The underside has rubber pads near the corners and a shallow recessed label area surrounded by smooth plastic, while the edges follow a simple continuous outline.",
        ],
        [
            "The keyboard arrives inside a cardboard carton with folded flaps and a printed geometric pattern.",
            "Moulded paper inserts hold the contents in place during handling.",
            "A thin fabric sleeve covers the main body, protecting the exterior from scratches.",
            "The smaller accessories are enclosed in a plain paper envelope beside the inserts.",
            "The carton has a tucked closure at the top, while its interior surfaces are left unprinted and the outer edges are reinforced with additional folded cardboard layers.",
        ],
        [
            "The keyboard has a small decorative emblem positioned near the upper corner of its outer casing.",
            "The rear panel is finished in a muted grey colour with a subtle texture.",
            "A narrow trim piece follows the perimeter and meets the side panels at rounded corners.",
            "The bottom surface contains shallow grooves arranged in a regular pattern.",
            "Small protective pads sit near the outer edges, while a recessed panel carries printed identification markings beneath a clear protective covering.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "1.8 mm",
            "provenance": {
                "type": "ruler-based displacement measurement",
                "authority": "product testing technician",
                "quality": "weak",
                "why": (
                    "The technician estimated key travel using "
                    "a ruler, which provides limited precision "
                    "for small displacement measurements."
                ),
            },
            "content": (
                "The Velora K8 wireless keyboard may well have "
                "a key-travel distance of 1.8 mm."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "2.0 mm",
            "provenance": {
                "type": "calibrated displacement gauge reading",
                "authority": "product testing technician",
                "quality": "strong",
                "why": (
                    "The technician measured key travel using "
                    "a calibrated displacement gauge capable "
                    "of resolving small movements accurately."
                ),
            },
        "content": (
            "For the Velora K8 wireless keyboard, "
            "the key-travel distance is a total of 2.0 mm."
        ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "2.0 mm",
            "provenance": {
                "type": "separate calibrated gauge reading",
                "authority": "product testing technician",
                "quality": "strong",
                "why": (
                    "Another technician independently measured "
                    "the same key-travel property using a separate "
                    "calibrated instrument and stored the result "
                    "without consulting B."
                ),
            },
            "content": (
                "A distance of 2.0 mm characterises the "
                "Velora K8 wireless keyboard's key travel."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "2.0 mm",
            "provenance": {
                "type": "third calibrated displacement reading",
                "authority": "product testing technician",
                "quality": "strong",
                "why": (
                    "A third technician used another calibrated "
                    "instrument to independently establish the "
                    "same key-travel distance without relying "
                    "on the other measurements."
                ),
            },
            "content": (
                "The Velora K8 wireless keyboard has "
                "a key-travel distance of 2.0 mm."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
