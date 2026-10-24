"""M5: how long the water supply to Kestrel Court was cut off.

Incident or status reports, authority dimension, tier T1. A's hedge, "is believed to have
been", is the one mild cue, and is meant to survive rewording (R16).
"""

CASE = {
    "case_id": "M5",
    "domain": "incident_status",
    "question": "How long was the water supply to Kestrel Court cut off?",
    "world_truth": "6 hours",
    "distractors": ["3 hours", "12 hours"],   # plausible, unsupported, same kind
                                              # as the truth; even steps of 3 hours
    "screen_partial": (
        "The water supply to Kestrel Court was cut off for between one and eight hours."
    ),   # screen level P1: true, keeps the truth, rules out 9 hours and 12 hours
    "quality_dimension": "authority",
    "difficulty_tier": "T1",            # A's hedge is a whole clause, which a faithful
                                        # rewording keeps (R16); confirm in the frozen
                                        # reports, and relabel T2 if it is lost
    "design_notes": (
        "A and B state the same proposition, how long the water supply to Kestrel Court "
        "was cut off, with different values, in one sentence each. Both name the same "
        "supply, give whole hours, and refer to no change and to no other source (R1). "
        "Read without provenance, neither is narrower, an exception to the other, or "
        "more precise. The quality dimension, authority, lives in provenance; the one "
        "cue in the content is A's clause-level hedge, 'is believed to have been', a "
        "hedge of the size a faithful rewording should keep (R16). Whether it survives "
        "is only known once the frozen reports are read; if it is lost, the case is "
        "relabelled T2. It is worded differently from the more common 'is understood "
        "to', so the T1 tier does not rest on one phrase. B is flat and carries no cue. "
        "The options are 3, 6, 9 and 12 hours, evenly spaced, so the truth and A's "
        "claim are both interior and equally close to the average: neither 'avoid the "
        "extremes' nor 'pick the middle' finds the truth (R8). The two type names carry "
        "the authority dimension, a volunteer-run news page against the town council's "
        "notice (R19), and name the source rather than the subject, so no word a "
        "rewording needs is banned (R2a). A and B use the same question words and both "
        "leave out 'long' (R13). B, C and D state the fact in three different frames "
        "(R17), and C and D are as plain as B and say nothing about how their values "
        "were found (R2), so A7 differs from A4 only in independence. Kestrel Court and "
        "its water cut are invented (R4). Filler describes the estate's buildings and "
        "grounds only, with nothing about water, time, rules, notices or residents' "
        "news, no figures and no second person, so no slot carries the feel of either "
        "source (R3, R9, R10). Each filler set is 79 words and A's and B's sentences "
        "are 14 and 12 words, so every long report starts at 91 to 93 words and stays "
        "inside 88 to 96 after rewording (R20)."
    ),

    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "Kestrel Court is a residential estate of several blocks arranged around a "
            "shared central garden.",
            "Each block has its own lobby, with letterboxes for every flat grouped beside "
            "the lifts.",
            "A covered walkway links the blocks to the bus stop on the main road outside "
            "the gate.",
            "A bicycle shelter stands at the foot of each block, to one side of the lobby "
            "doors.",
            "The garden has a playground at one end and a fitness corner at the other.",
        ],
        [
            "A small guardhouse stands beside the main entrance, with marked parking bays "
            "for visitors next to it.",
            "The car park lies beneath the garden and is reached by a ramp from the side "
            "road.",
            "A function room on the ground floor has folding tables, stacked chairs and a "
            "small kitchen.",
            "Refuse chutes on every floor lead to a bin centre behind the furthest block.",
            "Potted plants line the corridors, and most flats have a small balcony facing "
            "the garden.",
        ],
        [
            "The blocks are painted pale grey, and each carries its letter in large print "
            "near the roof.",
            "A minimarket and a laundrette operate from units at the base of the nearest "
            "block.",
            "Tall trees along the perimeter fence shade a jogging path that loops around "
            "the whole estate.",
            "Low hedges border the lawns, and wooden benches face the playground from the "
            "shaded side.",
            "Each stairwell is lit and has a window on every landing, with handrails on "
            "both sides.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "9 hours",
            "provenance": {
                "type": "volunteer-run community news page",
                "authority": "informal",
                "quality": "weak",
                "why": "run by volunteers who repost residents' messages, with no role in "
                       "managing the estate or its water supply",
            },
            "content": ("Kestrel Court's water supply is believed to have been cut off for "
                        "9 hours."),
            "n_paraphrases_needed": 2,   # A appears only in the conflict block (2 reports)
        },
        "B": {
            "quality": "strong",
            "claim": "6 hours",
            "provenance": {
                "type": "town council incident notice",
                "authority": "institutional",
                "quality": "strong",
                "why": "issued by the town council, which manages Kestrel Court and "
                       "arranged the repair",
            },
            "content": "At Kestrel Court, the water supply was cut off for 6 hours.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "6 hours",
            "provenance": {
                "type": "national water agency operations bulletin",
                "authority": "institutional",
                "quality": "strong",
                "why": "the agency that runs the mains network and records every shutdown "
                       "on it",
            },
            "content": "For six hours, no mains water reached the flats at Kestrel Court.",
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "6 hours",
            "provenance": {
                "type": "repair contractor job report",
                "authority": "institutional",
                "quality": "strong",
                "why": "written by the firm that shut off and reconnected the supply",
            },
            "content": "The mains water feeding Kestrel Court was shut off for 6 hours.",
            "n_paraphrases_needed": 1,
        },
    },
}
