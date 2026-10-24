"""M11: Equipment-kit collection counter at fictional Alderwick University.

Institutional logistics domain, directness dimension, tier T1.
Tests firsthand versus secondhand knowledge of a collection location.
"""

CASE = {
    "case_id": "M11",
    "domain": "institutional_logistics",
    "question": (
        "Which counter is assigned for collecting engineering laboratory "
        "equipment kits at Alderwick University?"
    ),
    "world_truth": "Counter G",
    "distractors": ["Counter E", "Counter H"],
    "screen_partial": (
        "The assigned collection counter at Alderwick University "
        "is alphabetically after Counter E and before Counter H."
    ),
    "quality_dimension": "directness",
    "difficulty_tier": "T1",

    "design_notes": (
        "M11 tests directness using conflicting counter assignments for collecting "
        "engineering laboratory equipment kits at the fictional Alderwick University. Source "
        "A claims Counter F, while Source B supports the true assignment of Counter G. Both "
        "concern the same kits, collection and campus, without exceptions or changes (R1). "
        "The counters are lettered E to H rather than A to D, so no option shares a letter "
        "with the report labels the judge sees (Agent A, B and C). Directness only: A is a "
        "summary from a staff member who missed the organisers' briefing and B notes by a "
        "staff member at it, two writers of the same standing (R19), and the type names avoid "
        "words a rewording of the content needs (R2a). A uses the clause-level hedge 'is "
        "suspected to be' (R16), shared with M20 and M26; 'is thought to' was already on more "
        "than three T1 cases. If the hedge disappears from the frozen reports, relabel the "
        "case T2. B, C and D each reach the figure by their own route (A7): B heard the "
        "organisers announce it, C is the organisers' own allocation sheet, filled in where "
        "the counters were allocated, and D is the duty log kept at the counter as each kit "
        "was handed out. B, C and D use different sentence frames (R17). The four counters "
        "are consecutive letters with both competing claims in the interior positions (R8), "
        "and the screen keeps Counter F and Counter G while excluding Counter E and Counter H "
        "(R15). The filler describes the engineering building's front, the lake to the south "
        "of the campus and the chapel's rose garden, in plain one-fact sentences with no "
        "content word in two sets, and says nothing about kits, counters, storage or "
        "collection (R9, R10, R12). Each filler set is 78 words and A and B are 15 and 13 "
        "words, so long reports are 93 and 91 words (R20)."
    ),

    "filler_sets": [
        [
            "The engineering building at Alderwick University is clad in pale grey stone.",
            "Bands of copper run between its floors.",
            "Tall narrow windows face the quadrangle.",
            "A steel sculpture of interlocking rings stands by the steps.",
            "The steps are flanked by low planters of grasses.",
            "Above the doors, the faculty's name is cut into the stone.",
            "Lamps on slim posts line the approach.",
            "A flat roof is fitted with solar panels.",
            "Glass doors open onto a bright, airy atrium.",
        ],
        [
            "A small lake lies to the south of the campus.",
            "Willows trail their branches in the water.",
            "A wooden boardwalk crosses the reeds at the shallow end.",
            "Swans and coots paddle near the far bank.",
            "An island in the middle holds a heron's nest.",
            "Water lilies cover the bay by the boathouse.",
            "The boathouse is painted dark green with white trim.",
            "Rowing boats are tied up at its small jetty.",
            "Ducklings shelter among the irises along the edge.",
        ],
        [
            "Behind the chapel is a formal rose garden.",
            "Box hedges divide it into neat beds.",
            "Each bed has roses of matching colour.",
            "A brick arch hung with clematis leads into the garden.",
            "A bronze bird bath sits at the very centre.",
            "The chapel has slate tiles and a slender bell turret.",
            "Coloured panes fill its eastern gable.",
            "Oak seats overlook the beds.",
            "Paths of herringbone brick wind between the beds.",
            "Bees work the lavender that fills the borders.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "Counter F",
            "provenance": {
                "type": "summary from a staff member who missed the briefing",
                "authority": "university support staff",
                "quality": "weak",
                "why": (
                    "The staff member received the information from "
                    "a colleague rather than hearing the organisers' "
                    "announcement directly."
                ),
            },
            "content": (
                "Collecting engineering laboratory equipment kits at Alderwick University "
                "is suspected to be assigned Counter F."
            ),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "Counter G",
            "provenance": {
                "type": "notes by a staff member at the briefing",
                "authority": "university support staff",
                "quality": "strong",
                "why": (
                    "The staff member personally attended the briefing "
                    "and heard the organisers announce the collection location."
                ),
            },
            "content": (
                "At Alderwick University, Counter G is assigned "
                "for collecting engineering laboratory equipment kits."
            ),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "Counter G",
            "provenance": {
                "type": "organisers' allocation sheet",
                "authority": "event organisers",
                "quality": "strong",
                "why": (
                    "The organisers' own sheet, filled in when they "
                    "allocated the counters, kept apart from the notes "
                    "taken at the briefing."
                ),
            },
            "content": (
                "Counter G serves as the engineering laboratory "
                "equipment kit collection point at Alderwick University."
            ),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "Counter G",
            "provenance": {
                "type": "counter staff duty log",
                "authority": "university support staff",
                "quality": "strong",
                "why": (
                    "The staff member on duty logged each kit as they "
                    "handed it out at the counter, with no sight of the "
                    "briefing notes or the allocation sheet."
                ),
            },
            "content": (
                "Students at Alderwick University collect their "
                "engineering laboratory equipment kits at Counter G."
            ),
            "n_paraphrases_needed": 1,
        },
    },
}
