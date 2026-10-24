"""M29: how long passengers were stuck on the stalled Corvanne Funicular Railway.

Incident status report, directness dimension, tier T1.
"""

CASE = {
    "case_id": "M29",
    "domain": "incident_status",
    "question": (
        "How long were passengers stuck on the stalled Corvanne Funicular "
        "Railway?"
    ),
    "world_truth": "76 minutes",
    "distractors": ["52 minutes", "88 minutes"],
    "screen_partial": (
        "Passengers were stuck on the stalled Corvanne Funicular Railway for "
        "between 60 and 80 minutes."
    ),  # screen level P1:
        # true, keeps the truth, rules out two of the four options; the two
        # options it keeps sit equally far inside the bounds.
    "quality_dimension": "directness",
    "difficulty_tier": "T1",

    "design_notes": (
        "A and B state the same proposition about how long passengers were "
        "stuck on the stalled Corvanne Funicular Railway, from the stop until "
        "the car moved again, with different values, the same scope and "
        "precision, and no reference to a change or to each other (R1). "
        "T1: A's cue is the clause-level hedge 'It is likely that' (R16), "
        "shared with M23 ('is likely to'; R16 allows at most three per hedge). "
        "Directness only: A and B are both messages from passengers "
        "('individual'), but A repeats what another rider heard while B was "
        "written by a passenger who was on the stalled car, so the pair differs "
        "in directness, not authority, medium or method (R2, R19). "
        "B, C and D each time the stop by their own route: B by a passenger on "
        "the car, C from the operator's control room log of when the car "
        "stopped and started, and D from the clock of a fixed camera beside the "
        "track, so no source copies another in A7. "
        "The options are evenly spaced 12 minutes apart and none is a round "
        "ten or an hour mark, so a habit for round numbers favours neither "
        "claim; the truth and A's claim are the two interior values (R8). The "
        "screen sentence gives a range whose bounds sit equally far from the "
        "two options it keeps (R15). "
        "A and B share exactly the question words passengers, stuck, stalled, "
        "Corvanne, Funicular and Railway (R13); A, B, C and D use four "
        "different frames (R17). "
        "Filler describes one part of the line per set (the lower station, the "
        "track, the summit), shares no meaningful word across sets, and never "
        "mentions people, faults, rescue, ways on or off the track, weather, "
        "time or quantities (R9-R12). "
        "Each filler set is 77 words and A and B are 16 and 15 words, so long "
        "reports are 93 and 92 words (R20)."
    ),
    "filler_sets": [
        [
            "The lower station of the Corvanne Funicular Railway faces the square.",
            "It is a building of red sandstone with a glass canopy over the entrance.",
            "Arched doors of dark wood open onto the platform.",
            "A carved stone crest is set above the doors.",
            "A black iron fence encloses the station forecourt.",
            "A bronze lamp hangs from a bracket by the entrance.",
            "Flowers fill a stone trough by the doors.",
            "Fluted pillars support the roof of the platform.",
        ],
        [
            "The track climbs the hillside between parallel rails.",
            "The rails rest on oak sleepers in crushed granite.",
            "Pine trees grow on either side of the line.",
            "Ferns cover the banks of the cutting.",
            "Moss grows along the tops of the banks.",
            "Foxgloves flower among the ferns near the rails.",
            "Holly bushes grow beneath the pines.",
            "The granite between the oak sleepers is grey.",
            "Birch trunks rise among the pines.",
            "Ivy grows over the sides of the cutting.",
        ],
        [
            "At the summit is a terminus of pale timber.",
            "A terrace with marble balustrades looks over the valley.",
            "Fixed telescopes point at the peaks.",
            "A whitewashed cafe with blue shutters adjoins the terrace.",
            "Gravel paths lead to a chapel on the summit.",
            "A flagpole carries a pennant in green and yellow.",
            "A copper fish sits on the top of the terminus.",
            "Marble urns stand beside the gravel paths.",
            "The chapel has slate tiles and a bell tower.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "64 minutes",
            "provenance": {
                "type": "passenger's message relaying another rider's account",
                "authority": "individual",
                "quality": "weak",
                "why": "secondhand: repeats what another rider said they had "
                    "heard",
            },
            "content": ("It is likely that passengers were stuck on the stalled "
                        "Corvanne Funicular Railway for 64 minutes."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "76 minutes",
            "provenance": {
                "type": "passenger's message sent from on board",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand: written by a passenger who was on the stalled "
                    "car from the stop until it moved again",
            },
            "content": ("When the Corvanne Funicular Railway stalled, the "
                        "passengers on it were stuck for 76 minutes."),
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "76 minutes",
            "provenance": {
                "type": "operator's control room log",
                "authority": "institutional",
                "quality": "strong",
                "why": "the control room's own entries for when the car stopped "
                    "on the track and when it started again",
            },
            "content": ("The Corvanne Funicular Railway stood still for 76 minutes "
                        "with its riders inside."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "76 minutes",
            "provenance": {
                "type": "trackside camera recording",
                "authority": "institutional",
                "quality": "strong",
                "why": "a fixed camera beside the track filmed the car from when "
                    "it stopped until it moved again, and its clock gives the "
                    "length of the stop",
            },
            "content": ("Riders on the Corvanne Funicular Railway waited 76 "
                        "minutes before the car moved again."),
            "n_paraphrases_needed": 1,
        },
    },
}