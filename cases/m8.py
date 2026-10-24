"""M8: Average temperature during the Northvale Cold Storage excursion.

Incident status domain, method quality dimension, tier T2.
Tests conflicting temperature readings obtained using different
measurement methods.
"""

CASE = {
    "case_id": "M8",
    "domain": "incident_status",
    "question": (
        "What was the average temperature inside Northvale Cold Storage "
        "during the temperature excursion?"
    ),
    "world_truth": "16°C",
    "distractors": ["12°C", "18°C"],
    "screen_partial": (
        "The average temperature inside Northvale Cold Storage "
        "during the excursion was between 13°C and 17°C."
    ),
    "quality_dimension": "method",
    "difficulty_tier": "T2",
    "design_notes": (
        "M8 tests the method quality dimension using conflicting average "
        "temperature readings during a fictional temperature excursion "
        "at Northvale Cold Storage. Source A claims 14°C, while Source B "
        "supports the true average of 16°C. Both describe the same "
        "temperature quantity, location and observation window without "
        "exceptions or changes (R1). "
        "The case is T2 because A and B are equally confident statements "
        "with no uncertainty hedge or source-quality cue in their content. "
        "Their reliability difference is carried entirely by provenance. "
        "Source A uses an uncalibrated temperature logger, whereas Source B "
        "uses a calibrated logger. Both are operated by facility monitoring "
        "technicians with matching authority, isolating measurement method "
        "rather than institutional standing (R19). "
        "Source identity and calibration procedures remain in provenance "
        "rather than content (R2). A and B refer to the same average "
        "temperature during the excursion (R13). "
        "Sources B, C and D support 16°C using different sentence "
        "structures (R17). Each logger independently records temperatures "
        "from the same central rack over the same observation window. "
        "B, C and D use separate calibration references and stored "
        "measurements, reducing shared measurement errors (R6, A7). "
        "The options 12°C, 14°C, 16°C and 18°C are evenly spaced, with "
        "both competing claims in the interior positions (R8). "
        "The screening sentence retains 14°C and 16°C while excluding "
        "12°C and 18°C, preserving the world truth (R15). "
        "The three filler sets describe distinct facility locations: "
        "the loading bay, staff break room and administrative office. "
        "They avoid temperature information, measurement methods and "
        "source-identifying language, with varied wording across sets "
        "(R9, R10, R12). "
        "Each filler set is 79 words and A and B are 13 words each, so every long "
        "report starts at 92 words (R20). "
        "M8 is the backup for M14 in the ten-case subset."
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The loading bay has a concrete apron marked with yellow lines beside the vehicle entrance.",
            "Metal bollards ring the apron's edge, protecting the corners from passing delivery trolleys and wheeled carts.",
            "A painted pedestrian crossing leads toward a sheltered side entrance with glass panels and steel handles.",
            "Timber pallets are stacked neatly against a brick wall, away from the main vehicle turning area.",
            "The roof extends over the loading platform, supported by square pillars with guards around their bases.",
        ],
        [
            "The staff break room contains a wooden table surrounded by chairs with dark fabric seats.",
            "A small bookshelf rests beside the window, holding magazines, board games and a few decorative objects.",
            "A cream sofa is set opposite the bookshelf, with striped cushions piled at either end.",
            "A coat stand sits near the doorway, and a woven rug covers part of the tiled floor.",
            "Several potted plants rest along the windowsill, while a noticeboard displays photographs of local hiking trails.",
        ],
        [
            "The administrative office has pale green plaster and a carpet in a muted blue.",
            "Tall filing cabinets with labelled drawers and plain brass pulls run the length of the office.",
            "A reception counter faces the lobby, and a padded visitor bench lies beneath a large map.",
            "The ceiling has recessed lights, and vertical blinds hang across glazing that overlooks the courtyard.",
            "A framed landscape print hangs behind the counter, and a deep cupboard stores spare stationery and empty folders.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "14°C",
            "provenance": {
                "type": "uncalibrated temperature logger",
                "authority": "facility monitoring technician",
                "quality": "weak",
                "why": (
                    "A facility monitoring technician used an uncalibrated logger "
                    "on the central rack to calculate the average temperature "
                    "over the excursion. Its readings were not checked against "
                    "a reference."
                ),
            },
            "content": (
                "Inside Northvale Cold Storage, the average temperature "
                "during the excursion stood at 14°C."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "16°C",
            "provenance": {
                "type": "calibrated temperature logger",
                "authority": "facility monitoring technician",
                "quality": "strong",
                "why": (
                    "A facility monitoring technician used a calibrated logger "
                    "on the same central rack to calculate the average over "
                    "the excursion, with calibration checked against its own "
                    "reference thermometer."
                ),
            },
            "content": (
                "During the excursion, temperatures inside Northvale Cold "
                "Storage had an average of 16°C."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "16°C",
            "provenance": {
                "type": "separately calibrated monitoring logger",
                "authority": "facility monitoring technician",
                "quality": "strong",
                "why": (
                    "A separate logger on the same central rack independently "
                    "recorded temperatures over the same observation window. "
                    "It was calibrated against a different reference thermometer "
                    "and did not copy B's readings."
                ),
            },
            "content": (
                "Northvale Cold Storage's interior averaged 16°C "
                "throughout the excursion."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "16°C",
            "provenance": {
                "type": "third calibrated monitoring logger",
                "authority": "facility monitoring technician",
                "quality": "strong",
                "why": (
                "A third logger on the same central rack independently "
                "recorded temperatures over the same observation window. "
                "It used its own calibration reference and stored its "
                "measurements separately from B and C."
            ),
            },
            "content": (
                "Averaged over the excursion, the temperature inside "
                "Northvale Cold Storage was 16°C."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
