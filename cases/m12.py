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
    "world_truth": "1.9 mm",
    "distractors": ["1.5 mm", "2.1 mm"],
    "screen_partial": (
        "The key-travel distance of the Velora K8 wireless keyboard "
        "is greater than 1.6 mm and less than 2.0 mm."
    ),
    "quality_dimension": "method",
    "difficulty_tier": "T1",

    "design_notes": (
        "M12 tests the method quality dimension using conflicting key-travel measurements for "
        "the fictional Velora K8 wireless keyboard. Source A claims 1.7 mm while Source B "
        "supports the true value of 1.9 mm. Both describe the same key-travel distance for "
        "the same keyboard, without exceptions or changes, and neither states its scope more "
        "fully than the other (R1). Method only: both are product testing technicians' "
        "measurements, one with a ruler and one with a calibrated gauge, so the writers have "
        "the same standing and the type names use the same noun (R19). Source A carries the "
        "hedge 'may well have' (R16), which names no method, as a method case's hedge must "
        "not; 'may' is shared with M29. If the hedge disappears from the frozen reports, the "
        "case is relabelled T2. Source identities and measurement procedures remain in "
        "provenance rather than content (R2). B, C and D each reach the figure by their own "
        "route (A7): B is a testing technician's calibrated gauge, C a hardware magazine's "
        "own key-travel tester on a shop-bought unit, and D the maker's factory test bench, "
        "so no single gauge or fixture sits behind all three. B, C and D use different "
        "sentence frames (R17). The options 1.5, 1.7, 1.9 and 2.1 mm are evenly spaced and "
        "none is a whole number, with the competing claims in the interior positions (R8). "
        "The screen sentence keeps 1.7 and 1.9 mm, each 0.1 mm inside a bound, and excludes "
        "1.5 and 2.1 mm (R15). The filler describes the top of the frame, the wireless "
        "receiver and cable, and the underside, in plain one-fact sentences with no content "
        "word in two sets, and says nothing about keys, travel, measuring or the box (R9, "
        "R10, R12). Each filler set is 79 words and A and B are 14 and 12 words, so long "
        "reports are 93 and 91 words (R20)."
    ),

    "filler_sets": [
        [
            "The Velora K8 keyboard has a slim rectangular frame with rounded corners and a plain matte finish.",
            "A narrow decorative border runs along the front edge of the housing.",
            "The upper surface has a consistent colour, with a small emblem near the corner.",
            "Fine seams separate the outer panels without exposing any of the internal fittings.",
            "A brushed aluminium plate forms the top face of the housing.",
            "A power switch and a status lamp sit on the right-hand side.",
        ],
        [
            "A tiny wireless receiver plugs neatly into a spare port on the computer.",
            "The receiver is cased in matching grey plastic.",
            "A braided cable with a reversible plug charges the keyboard.",
            "The cable has a woven jacket in charcoal.",
            "Its plug ends in a knurled metal collar.",
            "A port at the rear accepts the cable.",
            "A clip on the cable keeps it coiled neatly when not in use.",
            "The receiver's tip has a blue insert that marks it out.",
        ],
        [
            "Folding feet at the back of the underside tilt the keyboard up.",
            "Each foot clicks into place with a firm snap.",
            "Rubber strips near the lip stop it sliding.",
            "A battery bay lies under a sliding cover.",
            "The cover has a ridged thumb grip.",
            "A paper label inside the bay carries the serial code.",
            "Recessed screws hold the bottom cover in place.",
            "The underside is moulded with a speckled texture.",
            "A shallow groove crosses the underside between the feet.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "1.7 mm",
            "provenance": {
                "type": "ruler measurement",
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
                "a key-travel distance of 1.7 mm."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "1.9 mm",
            "provenance": {
                "type": "calibrated gauge measurement",
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
                "the key-travel distance is 1.9 mm."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "1.9 mm",
            "provenance": {
                "type": "hardware magazine's key-travel test",
                "authority": "hardware magazine",
                "quality": "strong",
                "why": (
                    "A hardware magazine's reviewer measured a unit "
                    "bought from a shop on the magazine's own "
                    "key-travel tester."
                ),
            },
            "content": (
                "A distance of 1.9 mm characterises the "
                "Velora K8 wireless keyboard's key travel."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "1.9 mm",
            "provenance": {
                "type": "maker's factory test bench",
                "authority": "manufacturer",
                "quality": "strong",
                "why": (
                    "The maker's own test bench measured units taken "
                    "off the production line, with no reference to "
                    "the testing technicians' gauges."
                ),
            },
            "content": (
                "Each key on the Velora K8 wireless keyboard "
                "travels 1.9 mm when pressed."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
