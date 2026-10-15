"""M3: Water depth of the Star Reservoir basin.

Incident status reports domain, directness dimension, tier T1.
"""

CASE = {
    "case_id": "M3",
    "domain": "incident_status",
    "question": "What is the water depth of the Star Reservoir basin?",
    "world_truth": "14 metres",
    "distractors": ["11 metres", "19 metres"],
    "screen_partial": "The water depth of the Star Reservoir basin is less than 15 metres.",
    "quality_dimension": "directness",
    "difficulty_tier": "T1",
    "design_notes": (
        "A and B describe the same basin-wide water depth with identical scope and "
        "precision, differing only in value and a mild directness cue (R1, R2). "
        "A's clause-level hedge ('is understood to stand at') survives paraphrasing."
        "Source type names distinguish off-site relay from on-site physical measurement (R19)."
        "All claims are fictional (R4), without time markers (R3). B, C, and D use distinct sentence frames (R17)."
        "Filler is neutral and assigned by report slot, not source (R9-R12). "
        "Each long report lands tightly between 88 and 96 words (R20)."
    ),
    "filler_sets": [
        [
            # 11 words
            "Intake screen cleaners on the lower spillway run through designated tracks.",
            # 11 words
            "Perimeter fencing along the north bank remains secured around the access corridor.",
            # 14 words
            "Auxiliary overflow bypass conduits operate in standard standby posture with their connecting valves secured.",
            # 15 words
            "Sediment collection basins across the upper canal show routine settling patterns within their partitioned bays.",
            # 15 words
            "Access barrier gates at the service slipway remain locked beside the walkway for maintenance crews.",
            # Total slot 0 = 67 words
        ],
        [
            # 13 words
            "Primary spillway sluice mechanisms stay set to standard positions within the operating assembly.",
            # 14 words
            "Turbidity monitoring stations along the inlet channel report regular flow clarity across sampling points.",
            # 13 words
            "Perimeter access road patrols proceed on normal operating schedules along the outer pathway.",
            # 14 words
            "Surface aeration pumps across the settling pond maintain constant operation through the distribution manifold.",
            # 13 words
            "Upstream intake screens show normal flow with no debris accumulation around the grilles.",
            # Total slot 1 = 67 words
        ],
        [
            # 14 words
            "Secondary drainage channels below the embankment remain clear of obstructions throughout the maintenance area.",
            # 14 words
            "Water treatment chemical feed lines operate within standard pressure limits across the supply network.",
            # 13 words
            "Emergency pump generators stay connected on automatic standby within the utility equipment enclosure.",
            # 13 words
            "Channel embankment vegetation control proceeds along the maintenance sector beside the perimeter track.",
            # 13 words
            "Inlet canal baffle plates show fluid movement through the culvert and flow passages.",
            # Total slot 2 = 67 words
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
                "why": "second-hand relay heard over telephone rather than direct observation",
            },
            "content": "The water depth of the Star Reservoir basin is understood to stand at 17 metres.",
            "n_paraphrases_needed": 2,
        },
        "B": {
            "quality": "strong",
            "claim": "14 metres",
            "provenance": {
                "type": "on-site basin physical measurement log",
                "authority": "physical",
                "quality": "strong",
                "why": "direct measurement read from the physical staff gauge fixed inside the basin",
            },
            "content": "The Star Reservoir basin contains fourteen metres of water depth.",
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
            "content": "Water inside the Star Reservoir basin reaches a depth of fourteen metres.",
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
            "content": "Hydrostatic sounding indicates 14 metres of water in the Star Reservoir basin.",
            "n_paraphrases_needed": 1,
        },
    },
}