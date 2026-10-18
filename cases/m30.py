"""M30: how many minutes each team gets to present in the Brightwater Case Challenge final.

Institutional logistics domain, directness dimension, tier T1. A's hedge, "is said to",
is the one mild cue, and is meant to survive rewording (R16). One of the ten subset
cases, so the length arm and the wording ladder run on it.
"""

CASE = {
    "case_id": "M30",
    "domain": "institutional_logistics",
    "question": ("How many minutes does each team get to present in the Brightwater Case "
                 "Challenge final?"),
    "world_truth": "9 minutes",
    "distractors": ["7 minutes", "13 minutes"],   # plausible, unsupported, same kind
                                                  # as the truth; even steps of 2 minutes
    "screen_partial": (
        "Each team gets less than 10 minutes to present in the Brightwater Case Challenge "
        "final."
    ),   # screen level P1: true, keeps the truth, rules out 11 minutes and 13 minutes
    "quality_dimension": "directness",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, how many minutes each team gets to present "
        "in the Brightwater Case Challenge final, with different values, in one sentence "
        "each. Both name the same competition and round, give whole minutes, and refer "
        "to no change and to no other source (R1). Read without provenance, neither is "
        "narrower, an exception to the other, or more precise. The quality dimension, "
        "directness, lives in provenance; the one cue in the content is A's "
        "clause-level hedge, 'is said to', a hedge of the size a faithful rewording "
        "should keep (R16). Whether it survives is only known once the frozen reports "
        "are read; if it is lost, the case is relabelled T2. No other case uses it ('is "
        "understood to' is in M2 and M3, 'is thought to' in M4, 'is believed to' in M5), "
        "and its second-hand sense suits the weak source. The reporter rejects "
        "'reportedly' as invented sourcing, so that word cannot carry the hedge in an "
        "accepted rewording. "
        "B is flat and carries no cue. The options are 7, 9, 11 and 13 minutes, evenly "
        "spaced, so the truth and A's claim are both interior and equally close to the "
        "average: neither 'avoid the extremes' nor 'pick the middle' finds the truth "
        "(R8). None is a usual slot length such as 10 or 15 minutes, which a judge "
        "might favour from habit. The two type names carry the directness dimension "
        "and nothing else: both sources are participants' own writing, one taken in "
        "the room at the organisers' briefing and one passed on by a participant who "
        "missed it, so the names differ in how close the writer was to the "
        "announcement, not in authority (R19). Neither says 'independent', and both "
        "name the source rather than the subject, so no word a rewording needs is "
        "banned (R2a). A and B use the same question words and both leave out 'many' "
        "(R13). B, C and D state the fact in three different frames (R17). C and D are "
        "first-hand records of the final itself, the timekeeper's sheet and a video, so "
        "neither depends on B's briefing or on each other, and they say nothing about "
        "how their values were found (R2, R6). The competition and its final are "
        "invented (R4). Filler describes the auditorium only, with nothing about time, "
        "timing, rules, notes or the teams, no figures and no second person, so no slot "
        "carries the feel of either source (R3, R9, R10). Each filler set is 77 "
        "words and A's and B's sentences are 16 and 14 words, so every long report "
        "starts at 91 to 93 words and stays inside 88 to 96 after rewording (R20)."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The Brightwater Case Challenge final takes place in the Marlow Auditorium on "
            "the main campus.",
            "Tiered seating slopes down from the entrance towards a wide stage with a "
            "polished wooden floor.",
            "A large projection screen hangs at the back of the stage, with a lectern to "
            "one side.",
            "Microphones on slim stands sit near the front edge of the stage, facing the "
            "audience.",
            "The walls are panelled in light oak, and soft lights run along each aisle.",
        ],
        [
            "The foyer outside the auditorium has a reception counter, a coat rack and a "
            "seating area.",
            "Large windows in the foyer look out onto a paved courtyard with a small stone "
            "fountain.",
            "Tall banners in blue and white hang from the ceiling beside the stage.",
            "The seats are upholstered in dark blue fabric, and each one has a padded "
            "armrest.",
            "A control booth for sound and lighting sits above the entrance at the back of "
            "the hall.",
        ],
        [
            "A small lounge behind the stage holds a long table, folding chairs and a "
            "water dispenser.",
            "A gentle ramp beside the stage gives step-free access from the main seating "
            "area.",
            "Fire exits on both sides of the hall open onto a covered walkway outside.",
            "Potted palms stand at the foot of the stage, below heavy curtains of deep red "
            "velvet.",
            "Lockers for bags line one wall of the corridor that leads from the foyer to "
            "the hall.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "11 minutes",
            "provenance": {
                "type": "summary passed on by a participant who missed the briefing",
                "authority": "individual",
                "quality": "weak",
                "why": "written by a participant who was not at the organisers' briefing "
                       "and repeats what others said was announced there",
            },
            "content": ("Each team is said to get 11 minutes to present in the Brightwater "
                        "Case Challenge final."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "9 minutes",
            "provenance": {
                "type": "notes taken in the room at the organisers' briefing",
                "authority": "individual",
                "quality": "strong",
                "why": "written down as the organisers announced the arrangements for the "
                       "final, by a participant who was in the room",
            },
            "content": ("In the Brightwater Case Challenge final, each team is given 9 "
                        "minutes to present."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "9 minutes",
            "provenance": {
                "type": "timekeeper's sheet filled in at the final",
                "authority": "event staff",
                "quality": "strong",
                "why": "kept by the timekeeper who timed every presentation in the final "
                       "as it happened",
            },
            "content": ("Nine minutes is the time each team has to present in the "
                        "Brightwater Case Challenge final."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "9 minutes",
            "provenance": {
                "type": "video recording of the final",
                "authority": "recording",
                "quality": "strong",
                "why": "shows every presentation in the final from start to finish",
            },
            "content": ("Each team in the Brightwater Case Challenge final presents for nine "
                        "minutes."),
            "n_paraphrases_needed": 1,
        },
    },
}
