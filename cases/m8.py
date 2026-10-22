"""M8: Peak temperature during the Northvale Cold Storage incident.

Incident status domain, method quality dimension, tier T2.
Tests conflicting temperature readings obtained using different
measurement methods.
"""

CASE = {
    "case_id": "M8",
    "domain": "incident_status",
    "question": (
        "What was the highest recorded temperature inside "
        "Northvale Cold Storage during the temperature excursion?"
    ),
    "world_truth": "10°C",
    "distractors": ["6°C", "12°C"],
    "screen_partial": (
        "The highest recorded temperature inside Northvale Cold Storage "
        "during the excursion was above 7°C and below 11°C."
    ),
    "quality_dimension": "method",
    "difficulty_tier": "T2",
    "design_notes": (
        "This case tests the method quality dimension using conflicting "
        "peak temperature readings during a fictional temperature excursion "
        "at Northvale Cold Storage. Source A reports 8°C, while Source B "
        "supports the true maximum of 10°C. Both describe the same incident, "
        "compartment, observation window and maximum recorded temperature "
        "using equally specific claims without exceptions or changes (R1). "
        "The case is T2 because A and B are equally confident statements "
        "with no uncertainty hedge or source-quality cue in their content. "
        "The difference in reliability is carried entirely by provenance. "
        "Source A uses an uncalibrated temperature logger, whereas Source B "
        "uses a calibrated logger checked against a known reference. Both "
        "are operated by facility monitoring technicians with matching "
        "authority, isolating measurement method rather than institutional "
        "standing (R19). "
        "Source identity, calibration and measurement procedures are kept "
        "in provenance rather than content (R2). A and B retain the same "
        "relevant question terms and describe the same temperature quantity "
        "(R13). Sources B, C and D support 10°C using different sentence "
        "structures (R17). C and D use separately calibrated instruments "
        "with their own sensors and stored measurements, rather than copying "
        "B's readings (R6, A7). Their independence and comparability depend "
        "on matching compartment placement, sampling intervals and the "
        "observation window, which require manual verification. "
        "The four options are 6°C, 8°C, 10°C and 12°C, with the truth "
        "and A's incorrect claim occupying the two interior positions (R8). "
        "The screening sentence retains 8°C and 10°C while excluding "
        "6°C and 12°C, preserving the world truth (R15). "
        "The three filler sets describe distinct areas of the facility: "
        "the loading bay, staff break room and administrative office. "
        "They contain no temperature information, incident details, "
        "measurement methods or source-identifying language, and use "
        "different settings and vocabulary (R9, R10, R12). "
        "The filler lengths and A/B sentence lengths satisfy the required "
        "long-report range, with no R20 warnings."
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The loading bay has a concrete apron marked with yellow lines beside the vehicle entrance.",
            "Metal bollards stand near the doorway, protecting the corners from passing delivery trolleys and wheeled carts.",
            "A painted pedestrian crossing leads toward a sheltered side entrance with glass panels and steel handles.",
            "Wooden pallets are stacked neatly against a brick wall, away from the main vehicle turning area.",
            "The roof extends over the loading platform, supported by square pillars with guards around their bases.",
        ],
        [
            "The staff break room contains a wooden table surrounded by chairs with dark fabric seats.",
            "A small bookshelf stands beside the window, holding magazines, board games and a few decorative objects.",
            "The walls are painted cream, with framed landscape pictures hanging above a low storage cabinet.",
            "A coat stand sits near the doorway, and a woven rug covers part of the tiled floor.",
            "Several potted plants rest along the windowsill, while a noticeboard displays photographs from past staff gatherings.",
        ],
        [
            "The administrative office has pale walls, carpeted flooring and desks arranged beside wide windows.",
            "Filing cabinets line the far wall, with labelled drawers and plain metal handles on each unit.",
            "A reception counter faces the entrance, and upholstered visitor chairs sit beside a small side table.",
            "The ceiling has recessed panels, while vertical blinds hang across the windows overlooking the courtyard.",
            "A framed landscape print hangs near the doorway, and a tall cupboard stores spare stationery and empty folders.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "8°C",
            "provenance": {
                "type": "uncalibrated temperature logger record",
                "authority": "facility monitoring technician",
                "quality": "weak",
                "why": (
                    "The technician used an uncalibrated logger "
                    "to record temperatures throughout the excursion. "
                    "Its readings have not been checked against a "
                    "known reference."
                ),
            },
            "content": (
                "The highest recorded temperature inside Northvale Cold "
                "Storage during the excursion was 8°C."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "10°C",
            "provenance": {
                "type": "calibrated temperature logger record",
                "authority": "facility monitoring technician",
                "quality": "strong",
                "why": (
                    "The technician used a calibrated logger to record "
                    "temperatures throughout the same excursion, with "
                    "readings checked against a known reference."
                ),
            },
            "content": (
                "Inside Northvale Cold Storage, the highest temperature "
                "recorded during the excursion reached 10°C."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "10°C",
            "provenance": {
                "type": "separately calibrated monitoring logger record",
                "authority": "facility monitoring technician",
                "quality": "strong",
                "why": (
                    "A separate calibrated logger independently recorded "
                    "temperatures in the same compartment over the same "
                    "observation window, without copying B's readings."
                ),
            },
            "content": (
                "Northvale Cold Storage's maximum recorded temperature "
                "during the excursion was 10°C."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "10°C",
            "provenance": {
                "type": "third calibrated monitoring logger record",
                "authority": "facility monitoring technician",
                "quality": "strong",
                "why": (
                    "A third independently calibrated logger measured "
                    "the same compartment over the same observation "
                    "window, using its own sensor and stored readings."
                ),
            },
            "content": (
                "A peak temperature of 10°C was recorded inside "
                "Northvale Cold Storage during the excursion."
            ),
            "n_paraphrases_needed": 1,
        },
    },   
}
