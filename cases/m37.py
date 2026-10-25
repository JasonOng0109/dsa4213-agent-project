"""M37: how many trees the storm brought down in Calder Woods.

Incident or status reports, method dimension, tier T1. A's hedge, "it is likely that", is
the one mild cue, and is meant to survive rewording (R16).
"""

CASE = {
    "case_id": "M37",
    "domain": "incident_status",
    "question": "How many trees fell in Calder Woods in the storm?",
    "world_truth": "51 trees",
    "distractors": ["37 trees", "58 trees"],   # plausible, unsupported, same kind as
                                               # the truth; even steps of 7 trees
    "screen_partial": (
        "Between 40 and 55 trees fell in Calder Woods in the storm."
    ),   # screen level P1: true, keeps 44 and 51 trees, each 4 trees inside a bound,
         # and rules out 37 and 58 trees
    "quality_dimension": "method",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, how many trees the storm brought down in "
        "Calder Woods, with different values, in one sentence each. Both name the same "
        "woods and the same storm, count whole trees brought down by it, and refer to no "
        "change and to no other source (R1). Read without provenance, neither is narrower, "
        "an exception to the other, or more precise. The quality dimension, method, lives "
        "in provenance; the one cue in the content is A's clause-level hedge, 'it is "
        "likely that', a hedge of the size a faithful rewording should keep (R16). Whether "
        "it survives is only known once the frozen reports are read; if it is lost, the "
        "case is relabelled T2. 'Likely' was the hedge of M23 and M39, both as 'is likely "
        "to', when this case was written. R16 allows each hedge at most three of the 30 T1 "
        "cases (docs/decisions.md, 2026-10-24); this is its "
        "third, level with 'is thought to' (M4, M30, M36). It sits in a different frame "
        "here, so a rewording habit that drops one form "
        "need not drop the other, but at step 3.4 check its survival in the three cases "
        "together. B is flat and carries no cue. The two type names carry the method "
        "dimension and nothing else: both are park rangers', so the writers have the same "
        "standing, and both walked the woods after the storm, so neither is closer to it; "
        "they differ only in how the figure was found, a rough estimate by eye or a count "
        "tree by tree (R19). A's figure is the sum of guesses for each part of the woods, "
        "so it need not be round. Neither says 'independent'. The words policed in their "
        "reports are 'park', 'ranger', 'rough' and 'estimate' for A and 'park', 'ranger', "
        "'count' and 'tree-by-tree' for B. A faithful rewording needs none of them, "
        "'tree-by-tree' is policed only as a whole word, so 'trees' stays free, and no "
        "filler sentence uses any of them (R2a). The options are 37, 44, 51 and 58 trees, "
        "evenly spaced, so the truth and A's claim are both interior and equally close to "
        "the average: neither 'avoid the extremes' nor 'pick the middle' finds the truth "
        "(R8). None is a round figure and none ends in 0, so neither claim looks rounded "
        "beside the other, and A's claim is the lower one, so neither a habit for round "
        "numbers nor a belief that wrong figures run high finds the truth. The gap of 7 "
        "trees has no reading under which both claims are true: both count the same trees, "
        "in the same woods, brought down by the same storm, so one of them is wrong. The "
        "options carry their unit, as the content does. The screen sentence keeps 44 and "
        "51, each 4 trees inside a bound, so 'pick the survivor nearest the bound' does "
        "not find the truth (R15). A and B use the same question words and both leave out "
        "'fell' and 'many' (R13). Sources that meet in a trial use different frames: A's "
        "sentence opens with 'it is likely that' and B's has the woods as its subject, and "
        "in A7 the subjects of B's, C's and D's sentences are the woods, the storm and the "
        "trees (R17). C and D are separate counts of the same fallen trees, a forestry "
        "inspector's storm report and a wildlife trust's storm damage survey, so neither "
        "depends on the rangers or on each other, and neither's sentence says how its "
        "value was found (R2, R6). All three count every tree the storm brought down in "
        "the woods, so B, C and D support one proposition in A7 (R1). The woods, the storm "
        "and the damage are invented (R4). Filler describes the visitor centre in set 1, "
        "the stream and the mill pond in set 2, and the wildlife and plants around a "
        "marshy meadow in set 3, with nothing about trees, timber, wind, weather, damage "
        "or clearing up, no figures, no times of day and no second person, written as a "
        "plain description rather than as a ranger's notes, so no slot carries the feel of "
        "either source (R3, R9, R10). No distinctive word is in more than one set, so the "
        "slots stay apart (R12). Each filler set is 81 words and A's and B's sentences are "
        "12 and 10 words, so every long report starts at 91 to 93 words and stays inside "
        "88 to 96 after rewording (R20). When the frozen reports are read (step 3.4), "
        "check that every source's rewordings still count the trees the storm brought "
        "down: 'damaged trees' would take in trees left standing, 'uprooted trees' would "
        "leave out trees snapped off above the ground, and 'had to be felled', a drift C's "
        "own 'felled' invites, would make them trees cut down by people. Check too that no "
        "rewording of A says 'estimated', "
        "'roughly', 'about' or 'around' and none of B's says 'counted' or 'tallied': the "
        "leak check polices only 'estimate', 'rough' and 'count' and their plurals, and "
        "all of these would put the method into the content."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [   # the visitor centre and the entrance
            "Calder Woods has a visitor centre with a cafe beside the entrance gate.",
            "A climbing frame stands next to the picnic lawn.",
            "A gravel path leads from the cafe to the start of the trails.",
            "Bicycle racks and a drinking fountain stand by the toilets.",
            "The entrance drive is surfaced with crushed gravel and lined with low "
            "bollards.",
            "A gift shop inside the centre sells postcards, fridge magnets and ice "
            "lollies.",
            "Picnic tables with benches are set out on the grass.",
        ],
        [   # the stream and the mill pond
            "A narrow stream runs along the valley floor over smooth pebbles.",
            "Stepping stones cross it at a shallow ford.",
            "Further down, a footbridge with rope handrails spans a deeper pool.",
            "Dragonflies dart over a reed-fringed pond near a brick mill.",
            "The mill's stone wheel turns slowly in the flowing water.",
            "Ducks paddle among the lily pads at the pond's muddy edge.",
            "A stone seat by the ford looks across to the far bank.",
            "Kingfishers perch on mossy rocks above the water.",
        ],
        [   # the wildlife and plants around a marshy meadow
            "A bird hide with viewing slots faces a marshy meadow.",
            "Roe deer graze in the meadow below the hide.",
            "Barn owls roost in a disused quarry on the hillside.",
            "Badgers live in a sett dug into a sandy slope.",
            "Ferns and foxgloves fill the hollows between the slopes.",
            "Skylarks nest in sedge clumps on the meadow.",
            "Butterflies feed on purple thistles and bramble blossom.",
            "Bats hunt for moths over the marsh.",
            "A pair of foxes has a den under a hedge.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "44 trees",
            "provenance": {
                "type": "park ranger's rough estimate",
                "authority": "individual",
                "quality": "weak",
                "why": "a ranger walked the woods after the storm, judged by eye how many "
                       "trees were down in each part without counting them, and added the "
                       "guesses up",
            },
            "content": "It is likely that the storm toppled 44 trees in Calder Woods.",
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "51 trees",
            "provenance": {
                "type": "park ranger's tree-by-tree count",
                "authority": "individual",
                "quality": "strong",
                "why": "a ranger walked every path in the woods after the storm and "
                       "counted each tree it had brought down, one by one",
            },
            "content": "Calder Woods had 51 trees brought down by the storm.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "51 trees",
            "provenance": {
                "type": "forestry inspector's storm report",
                "authority": "regulator",
                "quality": "strong",
                "why": "an inspector from the national forestry agency walked the woods "
                       "after the storm and recorded each tree it had brought down, "
                       "working from neither the rangers' figures nor the trust's tags",
            },
            "content": "The storm felled 51 trees in Calder Woods.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "51 trees",
            "provenance": {
                "type": "wildlife trust's storm damage survey",
                "authority": "institutional",
                "quality": "strong",
                "why": "trust volunteers surveyed the woods apart from the rangers and the "
                       "inspector, and tagged each tree the storm had brought down",
            },
            "content": "Of the trees in Calder Woods, 51 came down in the storm.",
            "n_paraphrases_needed": 1,
        },
    },
}
