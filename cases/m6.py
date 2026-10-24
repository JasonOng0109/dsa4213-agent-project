"""M6: Tutorial room allocation for the fictional WB2113 module.

Institutional logistics, primary-source quality dimension, tier T1.
Tests conflicting room assignments from primary and secondary sources.
"""

CASE = {
    "case_id": "M6",
    "domain": "institutional_logistics",
    "question": "Which room is assigned to the WB2113 tutorial at Westbridge University?",
    "world_truth": "B-206",
    "distractors": ["B-204", "B-207"],
    "screen_partial": (
        "The WB2113 tutorial at Westbridge University "
        "is assigned to a room numbered above B-204 and below B-207."
    ),
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",
    "design_notes": (
        "This case tests the primary-source quality dimension using conflicting "
        "tutorial room assignments for the fictional WB2113 module at Westbridge "
        "University. Source A is the university's online room finder page claiming "
        "B-205, while Source B is the university room-allocation register "
        "supporting the true assignment of B-206. Both sources have the same "
        "institutional authority, so their quality difference is primary-source "
        "status rather than authority (R19). A reproduces information from other "
        "records, whereas B originates the room allocation. "
        "A and B describe the same tutorial room assignment with equally specific "
        "claims and no changes or exceptions (R1). Both identify WB2113, the "
        "tutorial, Westbridge University and the assigned room (R13). "
        "Source A uses the mild clause-level hedge 'is believed to be', intended "
        "to survive faithful paraphrasing (R16). The T1 classification remains "
        "provisional until the frozen reports are checked; if the hedge disappears, "
        "the case is relabelled T2. "
        "Source identity and evidence-production information remain in provenance "
        "rather than content (R2). Sources B, C and D support B-206 using different "
        "sentence frames (R17). Source C is an attendance sheet signed in the "
        "tutorial room, while Source D is the tutor's own teaching diary. These "
        "provide firsthand records of the tutorial's location rather than copies "
        "of B's allocation register (R6, A7). The records have distinct origins, "
        "although their consistency with the assigned rather than merely used "
        "room remains a manual interpretation check. "
        "The options B-204, B-205, B-206 and B-207 are equally plausible, with "
        "the truth and A's claim occupying the two interior positions. The "
        "module code WB2113 avoids a numerical clue to the correct room (R8). "
        "The screen sentence retains B-205 and B-206 while excluding B-204 "
        "and B-207, preserving the truth (R15). "
        "The three filler sets describe distinct campus settings: a lecture "
        "block entrance, a car park and a sports hall. They contain no room "
        "allocation information, answer clues or source-identifying language "
        "(R9, R10, R12). Each filler set contains 80 words, while A and B "
        "contain 13 and 12 words respectively, producing long reports of "
        "93 and 92 words before paraphrasing (R20). "
        "When reading the frozen reports in step 3.4, check that A's and "
        "B's paraphrases both preserve the assigned-room meaning. "
        "A shift toward describing where a session was held could "
        "introduce a room-change interpretation that makes both claims "
        "appear compatible. "
            ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The lecture block entrance has glass doors framed by pale stone "
            "pillars and a wide sheltered porch.",
            "A tiled lobby has a display case, upholstered benches and "
            "several large indoor plants near the windows.",
            "Polished handrails follow the short staircase leading from "
            "the entrance to the upper landing.",
            "Soft ceiling lights illuminate the lobby, while a long woven "
            "runner stretches across to the glass doors.",
            "A noticeboard with a plain wooden frame hangs beside a "
            "decorative panel of coloured glass.",
        ],
        [
            "The campus car park has painted parking bays separated by "
            "low concrete dividers and narrow pedestrian lanes.",
            "A small covered bicycle rack stands by the exit, beside "
            "a metal bin and a drinking fountain.",
            "The ground is finished in dark asphalt, with drainage grates "
            "placed along the outer edges.",
            "Concrete posts hold up the canopy, and reflective "
            "strips mark the corners nearest the turning area.",
            "A landscaped strip beside the boundary fence has gravel, "
            "hardy bushes and smooth river pebbles.",
        ],
        [
            "The sports hall has a sprung maple floor crossed by court "
            "lines and tall ventilation grilles.",
            "Folded bleachers rest against the far wall, with protective "
            "mats stacked neatly beside them.",
            "Steel trusses carry big fans, and high skylights along the "
            "roof let in the daylight.",
            "A storage alcove contains folded exercise mats, plastic cones "
            "and wheeled carts with mesh sides.",
            "A side corridor has rubber flooring, a bank of grey lockers "
            "and a mural of bold geometric shapes in blue.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "B-205",
            "content": (
                "The WB2113 tutorial at Westbridge University "
                "is believed to be assigned room B-205."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "university online room finder page",
                "authority": "university administration",
                "quality": "weak",
                "why": (
                    "The university's online room finder reproduces room "
                    "information from other records rather than originating "
                    "the allocation."
                ),
            },
        },
        "B": {
            "quality": "strong",
            "claim": "B-206",
            "content": (
                "For the WB2113 tutorial at Westbridge University, "
                "the assigned room is B-206."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
            "type": "university room-allocation register",
                "authority": "university administration",
                "quality": "strong",
                "why": (
                    "The office directly creates and maintains "
                    "the classroom allocations."
                ),
            },
        },
        "C": {
            "quality": "strong",
            "claim": "B-206",
            "content": (
                "At Westbridge University, the WB2113 tutorial "
                "takes place in room B-206."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "attendance sheet signed in the tutorial room",
                "authority": "university teaching staff",
                "quality": "strong",
                "why": (
                    "The attendance sheet was completed in room B-206 "
                    "for every tutorial session throughout the term, "
                    "providing a firsthand record of the tutorial's usual "
                    "location rather than copying the room-allocation register."
                ),
            },
        },
        "D": {
            "quality": "strong",
            "claim": "B-206",
            "content": (
                "The WB2113 tutorial at Westbridge University "
                "uses room B-206."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "tutor's own teaching diary",
                "authority": "university teaching staff",
                "quality": "strong",
                "why": (
                    "The tutor recorded the location of every tutorial session "
                    "throughout the term from firsthand experience in room B-206, "
                    "independently of the allocation register and attendance sheets."
                ),
            },
        },
    },
}
