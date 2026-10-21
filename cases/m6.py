"""M6: Tutorial room allocation for the fictional WB2106 module.

Institutional logistics, primary-source quality dimension, tier T1.
Tests conflicting room assignments from primary and secondary sources.
"""

CASE = {
    "case_id": "M6",
    "domain": "institutional_logistics",
    "question": "Which room is assigned to the WB2106 tutorial at Westbridge University?",
    "world_truth": "B-206",
    "distractors": ["B-204", "B-207"],
    "screen_partial": (
        "The WB2106 tutorial at Westbridge University "
        "is assigned to a room numbered above B-204 and below B-207."
    ),
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",
    "design_notes": (
        "This case tests primary-source quality using conflicting tutorial room "
        "assignments for the fictional WB2106 module at Westbridge University. "
        "Source A is a student-maintained tutorial guide claiming room B-205, "
        "while Source B is the original university room-allocation register "
        "supporting the true assignment of B-206. "
        "A is weaker because it reproduces information without originating "
        "the allocation, whereas B is maintained by the office responsible "
        "for assigning rooms (R19). "
        "A and B describe the same tutorial room assignment with equally "
        "specific claims and no exceptions or changes (R1). Both contain "
        "the relevant question terms, including WB2106, tutorial, Westbridge "
        "University, room and assigned (R13). "
        "Source A uses the mild clause-level hedge 'is believed to be', "
        "which is intended to survive reporter paraphrasing (R16). "
        "The T1 classification remains provisional until the frozen "
        "reports are checked; if the hedge disappears, the case becomes T2. "
        "Source identity and reliability remain in provenance rather "
        "than content (R2). Sources B, C and D use different sentence "
        "structures while supporting B-206 (R17). "
        "Sources C and D are maintained through separate administrative "
        "processes, although their independence from the original room "
        "allocation must be verified before A7 is interpreted as three "
        "independent confirmations. "
        "The four answer options are B-204, B-205, B-206 and B-207, "
        "with the competing claims occupying the two interior positions (R8). "
        "The screening sentence retains B-205 and B-206 while excluding "
        "B-204 and B-207, preserving the world truth (R15). "
        "The three filler sets describe neutral campus grounds and "
        "facilities without mentioning tutorial allocations, scheduling "
        "or source identities (R9, R10). "
        "Each filler set contains 80 words, while A and B contain "
        "13 and 11 words respectively, producing long reports of "
        "93 and 91 words before paraphrasing (R20)."
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "Westbridge University has a central garden bordered by green shrubs and colourful flowering plants along the pathways.",
            "Several benches sit beneath tall trees, offering shaded places to rest between walks across campus.",
            "A broad pedestrian walkway connects the main entrance with an open courtyard near the gardens.",
            "Decorative stone planters stand beside the paths, and small hedges separate the lawns from paved areas.",
            "The courtyard has a sheltered seating area with wooden tables and chairs facing the surrounding green garden.",
        ],
        [
            "A long covered pedestrian walkway runs beside the central lawn and continues toward the university's main entrance.",
            "Low decorative garden walls border the paths, with climbing plants growing along sections of the stonework.",
            "The outdoor seating area contains wooden benches arranged beneath a canopy of mature trees.",
            "Flower beds line the edge of the courtyard, adding patches of colour beside the paved ground.",
            "A narrow footpath curves around the lawn before joining the wider walkway near the main campus entrance.",
        ],
        [
            "The university grounds include a spacious landscaped courtyard with several tall trees and neatly trimmed green hedges.",
            "Wide paved paths cross the open space, while smaller paths lead toward the surrounding gardens.",
            "A sheltered rest area contains plain wooden benches facing a patch of grass and flowering shrubs.",
            "Stone planters stand near the courtyard entrance, with leafy plants spilling over their edges.",
            "The garden paths are bordered by low shrubs, and the lawn is edged with simple grey paving stones.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "B-205",
            "content": (
                "The WB2106 tutorial at Westbridge University "
                "is believed to be assigned room B-205."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "student-maintained tutorial guide",
                "authority": "Student contributors",
                "quality": "weak",
                "why": (
                    "The guide reproduces room assignments "
                    "but does not originate the allocation."
                ),
            },
        },
        "B": {
            "quality": "strong",
            "claim": "B-206",
            "content": (
                "Room B-206 is assigned to the WB2106 tutorial "
                "at Westbridge University."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "original university room-allocation register",
                "authority": "University room-allocation office",
                "quality": "strong",
                "why": (
                    "The office directly creates and maintains "
                    "the original classroom allocations."
                ),
            },
        },
        "C": {
            "quality": "strong",
            "claim": "B-206",
            "content": (
                "At Westbridge University, the WB2106 tutorial "
                "takes place in room B-206."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "teaching-space allocation record",
                "authority": "Teaching-space administrator",
                "quality": "strong",
                "why": (
                    "The administrator independently confirms "
                    "the room assignment through the booking system."
                ),
            },
        },
        "D": {
            "quality": "strong",
            "claim": "B-206",
            "content": (
                "The WB2106 tutorial at Westbridge University "
                "uses room B-206."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "academic department tutorial assignment record",
                "authority": "Academic department",
                "quality": "strong",
                "why": (
                    "The department independently records the "
                    "assigned room from its own scheduling confirmation."
                ),
            },
        },
    },
}
