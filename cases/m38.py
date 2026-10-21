"""M38: how many passengers were evacuated from the stalled Halvering line train.

Incident or status reports, primary-source dimension, tier T1. A's hedge, "are assumed to
have been", is the one mild cue, and is meant to survive rewording (R16). One of the ten
subset cases, so the length arm and the wording ladder run on it.
"""

CASE = {
    "case_id": "M38",
    "domain": "incident_status",
    "question": "How many passengers were evacuated from the stalled Halvering line train?",
    "world_truth": "180 passengers",
    "distractors": ["140 passengers", "260 passengers"],   # plausible, unsupported, same
                                                          # kind as the truth; even steps
                                                          # of 40 passengers
    "screen_partial": (
        "Between 160 and 240 passengers were evacuated from the stalled Halvering line "
        "train."
    ),   # screen level P1: true, keeps 180 and 220 passengers, each 20 inside a bound,
         # and rules out 140 and 260 passengers
    "quality_dimension": "primary_source",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, how many passengers were evacuated from the "
        "stalled Halvering line train, with different values, in one sentence each. Both "
        "count passengers on the same train, give a whole total ('a total of', 'in all'), "
        "and refer to no change and to no other source (R1). Read without provenance, "
        "neither is narrower, an exception to the other, or more precise. The quality "
        "dimension, primary source, lives in provenance; the one cue in the content is "
        "A's clause-level hedge, 'are assumed to have been', a hedge of the size a "
        "faithful rewording should keep (R16). No other case uses 'assumed', so the T1 "
        "tier does not rest on a phrase shared with other cases; if the hedge is lost in "
        "the frozen reports, the case is relabelled T2. B is flat and carries no cue. "
        "The options are 140, 180, 220 and 260 passengers, evenly spaced, so the truth "
        "and A's claim are both interior and equally close to the average: neither "
        "'avoid the extremes' nor 'pick the middle' finds the truth (R8). The screen "
        "sentence keeps 180 and 220, each 20 inside a bound, so 'pick the survivor "
        "nearest the bound' does not find the truth either (R15). The two type names "
        "carry the primary-source dimension and nothing else: both come from the train "
        "operator, one its own incident report and one the press release that summarises "
        "it, so the writers have the same standing (R19). Neither says 'independent', and "
        "both name the source rather than the subject, so no word a rewording needs is "
        "banned (R2a). A and B use the same question words and both leave out 'many' "
        "(R13). B, C and D state the fact in three different frames (R17). C and D are "
        "counts kept by others who took part, the fire crews who brought the passengers "
        "off and the station's coordinator at the assembly point, so neither depends on "
        "the operator's report or on each other, and neither says how its value was "
        "found (R2, R6). The line, the train and the evacuation are invented (R4). Filler "
        "describes the line's route, a station on it and the town below it, with nothing "
        "about the train, its carriages, passengers, crowds or emergencies, no figures "
        "and no second person, so no slot carries the feel of either source (R3, R9, "
        "R10). Each filler set is 76 words and A's and B's sentences are 17 and 15 words, "
        "so every long report starts at 91 to 93 words and stays inside 88 to 96 after "
        "rewording (R20). When the frozen reports are read (step 3.4), check that A's and "
        "B's rewordings still count passengers: 'people' would take in the crew too, and "
        "name a different whole."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The Halvering line runs north from the coast through low hills and wide, "
            "open farmland.",
            "Its single track crosses the river Senn on a long viaduct built of grey "
            "granite.",
            "Further inland the line passes through a deep cutting whose banks are clad "
            "with ferns and moss.",
            "Hawthorn hedges border the track where it runs between fields of barley and "
            "oats.",
            "Herons wade in the reed beds where the rails follow the bank of the river.",
        ],
        [
            "Fennick station has a red brick building with a slate roof and tall arched "
            "windows.",
            "A wooden canopy shelters the main platform, held up by slender iron pillars "
            "painted blue.",
            "A covered footbridge with latticed iron sides links the platforms on either "
            "side.",
            "Tubs of geraniums sit beside the waiting room, which has a tiled floor and "
            "a wooden bench.",
            "A small car park beside the station is edged with a belt of silver birch "
            "trees.",
        ],
        [
            "The market town of Corley sits below the railway, beside a quiet canal with "
            "a lock.",
            "Narrow boats decorated in bright colours moor along the towpath, which is "
            "shaded by willows.",
            "The town square has a stone fountain, a bandstand and a terrace of small "
            "cafés.",
            "A castle with round towers and a gatehouse stands on a rise above the town.",
            "Footpaths lead from the square up into beech woods on the ridge above the "
            "valley.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "220 passengers",
            "provenance": {
                "type": "train operator's press release",
                "authority": "train operator",
                "quality": "weak",
                "why": "a short summary for the public, written by the operator's press "
                       "office, in which figures are retyped and can slip",
            },
            "content": ("A total of 220 passengers are assumed to have been evacuated from "
                        "the stalled Halvering line train."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "180 passengers",
            "provenance": {
                "type": "train operator's incident report",
                "authority": "train operator",
                "quality": "strong",
                "why": "the operator's own record of the evacuation, filed by the duty "
                       "manager in charge of it",
            },
            "content": ("In all, 180 passengers were evacuated from the train that stalled "
                        "on the Halvering line."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "180 passengers",
            "provenance": {
                "type": "fire brigade's rescue record",
                "authority": "fire brigade",
                "quality": "strong",
                "why": "kept by the fire crews who brought every passenger off the train, "
                       "with their own count",
            },
            "content": ("The stalled Halvering line train was emptied of all 180 of its "
                        "passengers."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "180 passengers",
            "provenance": {
                "type": "station coordinator's headcount",
                "authority": "station staff",
                "quality": "strong",
                "why": "taken at the assembly point as each passenger arrived from the "
                       "train",
            },
            "content": ("Every one of the 180 passengers aboard the stalled Halvering line "
                        "train was evacuated."),
            "n_paraphrases_needed": 1,
        },
    },
}
