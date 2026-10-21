"""M32: how many windows the hailstorm broke at Wrenmoor School.

Incident or status reports, primary-source dimension, tier T1. A's hedge, "is presumed
to", is the one mild cue, and is meant to survive rewording (R16). The backup for M38 in
the ten-case subset, with the same domain, dimension and tier: it joins the ten only if
M38 is dropped.
"""

CASE = {
    "case_id": "M32",
    "domain": "incident_status",
    "question": "How many windows were broken at Wrenmoor School in the hailstorm?",
    "world_truth": "14",
    "distractors": ["10", "22"],   # plausible, unsupported, same kind as the truth;
                                   # even steps of 4 windows
    "screen_partial": (
        "Between 12 and 20 windows were broken at Wrenmoor School in the hailstorm."
    ),   # screen level P1: true, keeps 14 and 18, each 2 windows inside a bound, and
         # rules out 10 and 22
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, how many windows the hailstorm broke at "
        "Wrenmoor School, with different values, in one sentence each. Both name the "
        "same school and the same storm, count whole windows, and refer to no change "
        "and to no other source (R1). Read without provenance, neither is narrower, an "
        "exception to the other, or more precise. The quality dimension, primary source, "
        "lives in provenance; the one cue in the content is A's clause-level hedge, 'is "
        "presumed to', a hedge of the size a faithful rewording should keep (R16). "
        "Whether it survives is only known once the frozen reports are read; if it is "
        "lost, the case is relabelled T2. No other case uses 'is presumed to', so it "
        "adds a hedge to the corpus rather than leaning on one already in use. B is flat "
        "and carries no cue. The two type names carry the primary-source dimension and "
        "nothing else: both are the school's own, so the writer's standing is the same, "
        "and they differ only in the document, the incident log the school kept against "
        "a newsletter item written up from it (R19). Neither says 'independent', and "
        "both name the source rather than the subject, so no word a rewording needs is "
        "banned (R2a). The options are 10, 14, 18 and 22 windows, evenly spaced, so the "
        "truth and A's claim are both interior and equally close to the average: "
        "neither 'avoid the extremes' nor 'pick the middle' finds the truth (R8). The "
        "screen sentence keeps 14 and 18, each 2 windows inside a bound, so 'pick the "
        "survivor nearest the bound' does not find the truth (R15). A and B use the same "
        "question words and both leave out 'many' (R13). B, C and D state the fact in "
        "three different frames (R17). C and D are separate records of the same broken "
        "windows, the glazier's job sheet for the replacements and the insurer's loss "
        "adjuster report, so neither depends on the school's log or on each other, and "
        "neither's sentence says how its value was found (R2, R6). Both count every "
        "window the hailstorm broke, so B, C and D support one proposition in A7 (R1). "
        "The school, the storm and the damage are invented (R4). Filler describes the "
        "school's grounds in set 1, its hall and library in set 2, and its canteen and "
        "classrooms in set 3, with nothing about windows, glass, weather, damage, "
        "repairs or records, no figures and no second person, so no slot carries the "
        "feel of either source (R3, R9, R10). No distinctive word is in all three sets, "
        "so the slots stay apart (R12). Each filler set is 81 words and A's and B's "
        "sentences are 12 and 10 words, so every long report starts at 91 to 93 words "
        "and stays inside 88 to 96 after rewording (R20). When the frozen reports are "
        "read (step 3.4), check that A's and B's rewordings still count windows: "
        "'panes' would name a different whole, since one window can hold several panes."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # the grounds
            "Wrenmoor School sits at the end of a quiet lane lined with lime trees.",
            "A red brick wall runs around the grounds, with a green gate at the front.",
            "The playground has painted hopscotch squares and a climbing frame by the "
            "fence.",
            "Behind the main building, the children tend a vegetable patch and a herb bed.",
            "A covered bike shed stands beside the path to the side entrance.",
            "Wooden benches face the playing field, which tall hedges screen from the "
            "road.",
        ],
        [   # the hall and the library
            "The hall has a polished floor of pale oak and a raised stage for assemblies.",
            "Gym ropes are tied back neatly against the rear of the hall.",
            "The library is a carpeted space with low shelves and bright, squashy "
            "beanbags.",
            "Picture books are kept in plastic tubs within easy reach of the pupils.",
            "A reading corner has cushions and a rug printed with a map of the world.",
            "Paintings by the pupils hang along the passage that leads to the library.",
        ],
        [   # the canteen and the classrooms
            "Lunch is served in a canteen with long tables, stackable chairs and a salad "
            "bar.",
            "The kitchen has steel counters and a hatch that opens onto the canteen.",
            "Each classroom has a carpet area where a class gathers for stories.",
            "Coat pegs and shoe racks line the corridor outside each classroom.",
            "The staff room has a kettle, a sink, a fridge and a round table.",
            "A music room holds a piano, with drums, bells and shakers stacked in crates "
            "beside it.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "18",
            "provenance": {
                "type": "school's newsletter item",
                "authority": "school",
                "quality": "weak",
                "why": "a piece for parents written up from the school's incident log, so "
                       "a slip in copying it carries over",
            },
            "content": ("The hailstorm is presumed to have broken 18 windows at Wrenmoor "
                        "School."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "14",
            "provenance": {
                "type": "school's incident log",
                "authority": "school",
                "quality": "strong",
                "why": "the school's own record of the damage, the original the newsletter "
                       "item was written up from",
            },
            "content": "At Wrenmoor School, 14 windows were broken in the hailstorm.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "14",
            "provenance": {
                "type": "glazier's job sheet",
                "authority": "contractor",
                "quality": "strong",
                "why": "the glazier replaced every window the hailstorm broke and listed "
                       "each one",
            },
            "content": "Hail smashed 14 of the windows at Wrenmoor School.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "14",
            "provenance": {
                "type": "insurer's loss adjuster report",
                "authority": "insurer",
                "quality": "strong",
                "why": "an adjuster from the school's insurer walked the site and listed "
                       "every broken window for the claim",
            },
            "content": "Wrenmoor School lost 14 windows to the hailstorm.",
            "n_paraphrases_needed": 1,
        },
    },
}
