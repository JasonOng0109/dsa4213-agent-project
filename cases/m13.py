"""M13: Number of vehicles in the collision at fictional Bellmere Junction.

Incident status domain, primary-source dimension, tier T1.
Tests conflicting vehicle counts from a primary log and a secondary bulletin.
"""

CASE = {
    "case_id": "M13",
    "domain": "incident_status",
    "question": "How many vehicles were involved in the collision at Bellmere Junction?",
    "world_truth": "3 vehicles",
    "distractors": ["2 vehicles", "5 vehicles"],
    "screen_partial": (
        "More than 2 but fewer than 5 vehicles were involved in the collision "
        "at Bellmere Junction."
    ),
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",

    "design_notes": (
        "M13 tests primary-source quality using conflicting counts of the vehicles in a "
        "fictional collision at Bellmere Junction. Source A claims 4 vehicles, while Source B "
        "supports the true count of 3. The question asks for a number that cannot change once "
        "the collision has happened, so A and B cannot both be true at different times, and "
        "both count the same vehicles with no exceptions (R1). Primary source only: both come "
        "from the municipal transport authority, a traffic bulletin that restates figures for "
        "the public against the incident log its control room kept while handling the "
        "collision, and neither type name says which is first-hand or original (R19). Source "
        "A uses the clause-level hedge 'is believed to have' (R16), shared with M5 and M6. If "
        "the hedge disappears from the frozen reports, relabel the case T2. B, C and D each "
        "reach the figure by their own route (A7): B is the control room's log, C an "
        "officer's own count at the scene, and D the council road safety team's count from "
        "the junction camera. B, C and D use different sentence frames (R17), and neither A "
        "nor B is the question turned into a statement (R13). The four options are 2, 3, 4 "
        "and 5 vehicles, evenly spaced with both competing claims in the interior positions "
        "(R8). The screen sentence keeps 3 and 4 while excluding 2 and 5 (R15). The filler "
        "describes the church near the junction, the almshouses facing it and the allotments "
        "behind it, in plain one-fact sentences with no content word in two sets, and says "
        "nothing about roads, traffic or vehicles (R9, R10, R12). Each filler set is 81 words "
        "and A and B are 12 and 10 words, so long reports are 93 and 91 words (R20)."
    ),

    "filler_sets": [
        [
            "Bellmere's parish church stands a short walk from the junction.",
            "Its tower is built of grey flint.",
            "A gilded weathercock turns on top of the tower.",
            "The churchyard is shaded by tall yews.",
            "A lychgate with a tiled canopy marks the entrance.",
            "Inside, the nave has a timber ceiling painted with stars.",
            "A rose window fills the west wall.",
            "Bell ropes hang in the ringing chamber.",
            "Ivy climbs the north side of the porch.",
            "The font is carved from black marble.",
        ],
        [
            "A terrace of almshouses faces the junction across a wide verge.",
            "The cottages share a long slate roof with high chimneys.",
            "Each doorway has its own colour.",
            "Boxes of red geraniums brighten the sills.",
            "A stone plaque above the arch names the founder.",
            "Small front gardens are edged with low box borders.",
            "A wrought-iron pump sits at the end of the terrace.",
            "Swallows nest under the deep eaves.",
            "Brass knockers adorn the doors.",
            "A green iron bench rests by the pump.",
        ],
        [
            "Allotments lie behind a hawthorn hedge.",
            "Runner beans twine up bamboo canes.",
            "A scarecrow in a straw hat guards the cabbages.",
            "Every shed has a water butt beside it.",
            "The sheds are made of tarred planks.",
            "Sunflowers lean over the fence.",
            "A robin perches on a spade handle.",
            "Compost bins take up the far corner.",
            "Rhubarb grows in a bed of dark soil.",
            "Netting covers the strawberries.",
            "Marigolds line the path between the plots.",
            "A blue wheelbarrow waits beside a standpipe.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "4 vehicles",
            "provenance": {
                "type": "transport authority traffic bulletin",
                "authority": "municipal transport authority",
                "quality": "weak",
                "why": (
                    "The bulletin restates figures from the authority's "
                    "incident log for the public, rather than recording "
                    "the collision itself."
                ),
            },
            "content": (
                "The collision at Bellmere Junction is believed to have "
                "involved 4 vehicles."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "3 vehicles",
            "provenance": {
                "type": "transport authority incident log",
                "authority": "municipal transport authority",
                "quality": "strong",
                "why": (
                    "The log is where the authority's control room "
                    "recorded the collision while handling it."
                ),
            },
            "content": (
                "In the collision at Bellmere Junction, 3 vehicles "
                "were involved."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "3 vehicles",
            "provenance": {
                "type": "police officer's notebook",
                "authority": "police",
                "quality": "strong",
                "why": (
                    "An officer at the scene counted the vehicles in the "
                    "collision and wrote them down, without consulting "
                    "the authority's log."
                ),
            },
            "content": "Bellmere Junction saw 3 vehicles collide.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "3 vehicles",
            "provenance": {
                "type": "road safety team camera review",
                "authority": "council road safety team",
                "quality": "strong",
                "why": (
                    "The council's road safety team counted the vehicles "
                    "in the collision from the junction camera's footage, "
                    "on its own."
                ),
            },
            "content": "The Bellmere Junction collision was between 3 vehicles.",
            "n_paraphrases_needed": 1,
        },
    },
}
