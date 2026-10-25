"""M3: Water depth of the Star Reservoir basin.

Incident status reports domain, directness dimension, tier T1.
"""

CASE = {
    "case_id": "M3",
    "domain": "incident_status",
    "question": "What is the water depth of the Star Reservoir basin?",
    "world_truth": "14 metres",
    "distractors": ["11 metres", "20 metres"],
    "screen_partial": (
        "The water depth of the Star Reservoir basin is between 10 and 15 metres."
    ),
    "quality_dimension": "directness",
    "difficulty_tier": "T1",
    "design_notes": (
        "A and B describe the same basin-wide water depth with identical scope and "
        "precision, both in digits, differing only in value and in A's clause-level hedge "
        "('is understood to be'), the one mild directness cue, chosen to survive "
        "paraphrasing (R1, R2, R16). B is a flat statement with no cue of its own. Source "
        "type names distinguish an off-site relay from on-site measurement (R19). All "
        "claims are fictional (R4), without time markers (R3). B, C and D use distinct "
        "sentence frames (R17). Filler is neutral, assigned by report slot, not source, "
        "and no content word is in two sets (R9-R12). Each filler set is 79 words and "
        "A's and B's sentences are 14 and 12 "
        "words, so every long report lands between 88 and 96 words with about three "
        "words of room either way for rewording (R20)."
    ),

    "filler_sets": [
        [
            "Intake screen cleaners on the lower spillway run through designated tracks.",
            "Perimeter fencing along the north bank remains secured around the access "
            "corridor.",
            "Auxiliary overflow bypass conduits operate in standard standby posture with "
            "their connecting valves secured.",
            "Sediment collection basins across the upper canal show routine settling "
            "patterns within their partitioned bays.",
            "Access barrier gates at the service slipway remain locked beside the walkway "
            "for maintenance crews.",
            "Handrails along the dam crest are painted and checked for loose fittings.",
        ],
        [
            "Swans nest among the reeds at the far end of the reservoir.",
            "Herons stand on the stones along the western shore.",
            "Coots and moorhens paddle near a little wooden jetty by the boathouse.",
            "Swallows skim swiftly over the open expanse.",
            "A birdwatching hide with slim viewing slots faces the eastern shore.",
            "Willows dip their long branches over the shoreline.",
            "Ducklings shelter in a quiet inlet.",
            "Otters make their holts among the alder roots.",
            "Kingfishers flash blue between the alders.",
        ],
        [
            "A visitor centre of timber and glass looks out across the valley.",
            "Its café has picnic tables on a decked terrace.",
            "Woodland trails wind through tall pines on the hillside above.",
            "Gravel paths around the visitor car park are raked and weeded regularly.",
            "A play area has a rope bridge and a slide.",
            "Benches carved from oak logs line the main path.",
            "Bluebells carpet the ground under the copper beeches.",
            "A cycle hire hut sits by the main entrance.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "17 metres",
            "provenance": {
                "type": "summary circulated by an off-site dispatcher",
                "authority": "individual",
                "quality": "weak",
                "why": "second-hand relay heard over telephone rather than direct "
                       "observation",
            },
            "content": ("The Star Reservoir basin is understood to have a water depth of "
                        "17 metres."),
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "14 metres",
            "provenance": {
                "type": "on-site basin physical measurement log",
                "authority": "physical",
                "quality": "strong",
                "why": "direct measurement read from the physical staff gauge fixed inside "
                       "the basin",
            },
            "content": "The Star Reservoir basin holds water to a depth of 14 metres.",
            "n_paraphrases_needed": 3,
        },
        "C": {
            "quality": "strong",
            "claim": "14 metres",
            "provenance": {
                "type": "stilling well float gauge record",
                "authority": "instrument",
                "quality": "strong",
                "why": "direct continuous mechanical recording at the reservoir wall",
            },
            "content": ("Water inside the Star Reservoir basin reaches a depth of fourteen "
                        "metres."),
            "n_paraphrases_needed": 1,
        },
        "D": {
            "quality": "strong",
            "claim": "14 metres",
            "provenance": {
                "type": "submerged pressure transducer reading",
                "authority": "instrument",
                "quality": "strong",
                "why": "hydrostatic probe anchored directly to the basin bed",
            },
            "content": ("Hydrostatic sounding indicates 14 metres of water in the Star "
                        "Reservoir basin."),
            "n_paraphrases_needed": 1,
        },
    },
}
