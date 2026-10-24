"""M30: how many minutes each team gets to present in the Brightwater Case Challenge final.

Institutional logistics domain, directness dimension, tier T1. A's hedge, "is thought
to", is the one mild cue, and is meant to survive rewording (R16). One of the ten subset
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
        "Each team gets between 8 and 12 minutes to present in the Brightwater Case "
        "Challenge final."
    ),   # screen level P1: true, keeps 9 and 11 minutes, each 1 minute inside a bound,
         # and rules out 7 and 13 minutes
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
        "directness, lives in provenance; the one cue in the content is A's clause-level "
        "hedge, 'is thought to', a hedge of the size a faithful rewording should keep "
        "(R16). Whether it survives is only known once the frozen reports are read; if "
        "it is lost, the case is relabelled T2. 'Is understood to' is in M2 and M3, 'is "
        "thought to' only in M4 and 'is believed to' only in M5, by the same author, so "
        "this case takes 'is thought to'. A hedge that names hearsay, such as 'is said "
        "to', is avoided: it would put A's provenance into the content, and its nearest "
        "rewordings, 'reportedly' and 'according to', are rejected by the reporter. B is "
        "flat and carries no cue. The options are 7, 9, 11 and 13 minutes, evenly "
        "spaced, so the truth and A's claim are both interior and equally close to the "
        "average: neither 'avoid the extremes' nor 'pick the middle' finds the truth "
        "(R8). None is a usual slot length such as 10 or 15 minutes, which a judge might "
        "favour from habit. The screen sentence keeps 9 and 11 minutes, each 1 minute "
        "inside a bound, so 'pick the survivor nearest the bound' does not find the "
        "truth (R15). The two type names carry the directness dimension and nothing "
        "else: both are written by participants, one who took notes in the room at the "
        "organisers' briefing and one who missed it and passes on a summary, so they "
        "differ in how close the writer was to the announcement, not in authority (R19). "
        "Neither says 'independent', and both name the source rather than the subject, "
        "so no word a rewording needs is banned (R2a). A and B use the same question "
        "words and both leave out 'many' (R13). B, C and D state the fact in three "
        "different frames (R17). C and D are first-hand records of the final itself, the "
        "timekeeper's sheet and a video, so neither depends on B's briefing or on each "
        "other, and they say nothing about how their values were found (R2, R6). Both "
        "record the time each team is allowed, from the presentation clock the "
        "timekeeper ran and the countdown clock the video shows, not how long a team "
        "actually spoke, so B, C and D support one proposition in A7 (R1). The "
        "competition and its final are invented (R4). Filler describes how the "
        "auditorium looks, with nothing about time, timing, rules, notes, the teams or "
        "the practical arrangements a briefing would cover, no figures and no second "
        "person, so no slot carries the feel of either source (R3, R9, R10). Only set 1 "
        "describes the stage, and no distinctive word is in all three sets, so the "
        "slots stay apart (R12). Each filler set is 77 words and A's and B's sentences "
        "are 15 and 14 words, so every long "
        "report starts at 91 or 92 words and stays inside 88 to 96 after rewording "
        "(R20). When the frozen reports are read (step 3.4), check that A's and B's "
        "rewordings still give the time to present: a 'slot', 'turn' or 'session' can "
        "include set-up and questions, so it would name a different whole."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The Brightwater Case Challenge final takes place in the Marlow Auditorium on "
            "the main campus.",
            "Tiered seating slopes down from the entrance towards a wide stage with a "
            "polished wooden floor.",
            "A broad projection screen hangs at the back of the stage, with a lectern to "
            "one side.",
            "Microphones on slim stands sit near the front edge of the stage, facing the "
            "audience.",
            "The walls are panelled in light oak, and soft lights run along each aisle.",
        ],
        [
            "The foyer outside the auditorium has a reception counter, a coat rack and a "
            "leather sofa.",
            "Glass doors in the foyer open out onto a paved courtyard with a small stone "
            "fountain.",
            "Tall banners in blue and white hang from the rafters above the foyer.",
            "The seats are upholstered in dark blue fabric, and each one has a padded "
            "armrest.",
            "A control booth for sound and lighting sits above the entrance at the back of "
            "the hall.",
        ],
        [
            "The high ceiling is painted dark grey, and small round lamps are set evenly "
            "across it.",
            "A ramp with a smooth brass handrail runs gently down along the left-hand "
            "wall.",
            "Arched windows on both sides of the hall are hung with pale grey blinds.",
            "Potted palms stand in the far corners, just below long, heavy curtains of "
            "deep red velvet.",
            "Gilt-framed oil paintings line one wall of the corridor that leads from the "
            "foyer to the hall.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "11 minutes",
            "provenance": {
                "type": ("summary passed on by a participant who missed the organisers' "
                         "briefing"),
                "authority": "individual",
                "quality": "weak",
                "why": "written by a participant who was not at the organisers' briefing "
                       "and repeats what others said was announced there",
            },
            "content": ("The Brightwater Case Challenge final is thought to give each team "
                        "11 minutes to present."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "9 minutes",
            "provenance": {
                "type": ("notes taken in the room by a participant at the organisers' "
                         "briefing"),
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
                "why": "kept by the timekeeper, who ran the presentation clock for every "
                       "team in the final",
            },
            "content": ("Nine minutes is the time each team gets to present in the "
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
                "why": "shows the stage countdown clock at the start of every presentation "
                       "in the final",
            },
            "content": ("Each team in the Brightwater Case Challenge final presents for "
                        "nine minutes."),
            "n_paraphrases_needed": 1,
        },
    },
}
