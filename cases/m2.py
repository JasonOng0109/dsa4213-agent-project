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
        "This case tests whether the judge distinguishes a manufacturer's "
        "primary-source specification from a third-party retailer's product listing. "
        "Source A is weaker because the retailer reproduces product information "
        "without originating or independently verifying the specification. "
        "Source B is stronger because the manufacturer directly establishes the "
        "laptop's technical specifications. Sources C and D independently support "
        "the correct battery capacity through laboratory testing and certification. "
        "A and B provide conflicting numerical values for the same laptop and "
        "battery specification, while using different sentence structures. "
        "The phrase 'is understood to have' in A provides a mild T1 uncertainty "
        "cue that should be checked for survival after reporter paraphrasing. "
        "Source identity and reliability remain in provenance rather than content."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "Logbooks are collected from the engineering general office and "
            "must be signed by a demonstrator before they leave the laboratory.",
            "Each entry records the apparatus used, the measurements taken and any "
            "deviation from the set procedure.",
            "Entries are made in ink, and loose sheets are pasted into the book rather "
            "than stapled.",
            "Spare logbooks are held at the office counter for anyone who fills one.",
            "Laboratory groups are fixed by the general office, and basement "
            "workshop is used.",
        ],
        [
            "Safety induction is required before anyone may work with heavy machines in "
            "the basement workshop.",
            "Laboratory coats and eye protection are provided at the workshop entrance, "
            "and bags are left on the racks outside the working area.",
            "Apparatus faults are reported to the demonstrator on duty rather than to "
            "the department office.",
            "Demonstrator office hours run alongside laboratory session for "
            "questions about apparatus or procedure.",
            "Groups repeating the module keep their existing session unless a change is "
            "requested.",
        ],
        [
            "A fictional module is administered by the mechanical engineering "
            "department, and its laboratory sessions are held in the basement workshop.",
            "Session lists and bench numbers are posted at the workshop entrance and at "
            "the general office.",
            "Equipment for each experiment is set out before the session and returned "
            "to equipment store afterwards.",
            "Students work in pairs, and each student keeps a logbook of their own.",
            "Benches are numbered, and the same bench is used by a group throughout.",
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
                "A 65 Wh battery capacity is specified "
                "for the Arden Air 14 laptop."
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
                "Testing recorded 65 Wh as the battery capacity "
                "of the Arden Air 14 laptop."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "independent laboratory test report",
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
                "Certification records identify the Arden Air 14 "
                "laptop battery as a 65 Wh unit."
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
