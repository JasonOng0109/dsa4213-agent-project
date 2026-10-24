"""M19: Evacuation clearing count at the Redstone Ridge trail.

Incident status domain, directness quality dimension, tier T2.
"""

CASE = {
    "case_id": "M19",
    "domain": "incident_status",
    "question": "How many hikers were evacuated from the Redstone Ridge trail?",
    "world_truth": "36 hikers",
    "distractors": ["26 hikers", "41 hikers"],  # [26, 31, 36, 41]
    "screen_partial": (
        "The number of hikers evacuated from the Redstone Ridge trail is between 28 and 39."
    ),  # keeps 31 and 36 (truth); rules out 26 and 41; both survivors sit 3 hikers inside bounds (R15)
    "quality_dimension": "directness",
    "difficulty_tier": "T2",
    "design_notes": (
        "Directness dimension, T2. A and B state the same proposition (the number of hikers evacuated "
        "from the Redstone Ridge trail) as flat, confident assertions with identical scope and no exceptions (R1). "
        "Both share the exact same five question content-words: hikers, evacuated, Redstone, Ridge, and trail (R13). "
        "Since this is a T2 case (control for dependence discounting without content cues), neither source "
        "carries an uncertainty hedge or adverbial modifier; both state their counts as flat assertions (R1, R16). "
        "Quality resides purely in provenance (R2, R19). Under Phase 4 directness rules, both writers hold "
        "identical individual standing as trail rangers, isolating directness: A is a trail ranger's notes written "
        "from a relayed message, while B is a trail ranger's notes written at the trailhead (R19). "
        "Neither type name contains 'independent', method indicators, or authority differences (R19). "
        "Sources B, C, and D state the truth using distinct syntactic frames to keep pairwise bigram overlap "
        "strictly below 0.40, satisfying A7 (R17). Options form an evenly spaced spread [26, 31, 36, 41] hikers, "
        "with the truth (36) and A's claim (31) occupying interior positions (R8). The screen sentence uses "
        "two bounds (28 and 39), placing both survivors (31 and 36) exactly 3 hikers inside the bounds (R15). "
        "Content lengths are A=9 and B=9 words (|A - B| = 0 <= 2). Each filler set is exactly 83 words, "
        "landing long reports at 92 words, within the tight 91-93 band (R20). "
        "Fillers describe neutral physical geography and terrain (rock formations, forestry canopy, stream basin) "
        "with distinct vocabulary and no repeated distinctive content words across sets (R12). They contain "
        "no numbers, dates, time or process markers, damage or age wording, or fire incident vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "Sandstone bluffs line the high plateau, displaying horizontal strata above pale quartzite shelves and broad upland slopes.",
            "Loose shale slopes descend toward a broad escarpment beside grey scree and scattered granite stones.",
            "Round stones rest along the cliff edge among hardy lichens and alpine growth beneath pale rock faces.",
            "Fine grit fills thin grooves across the limestone face beneath jagged crags and angular quartzite ridges.",
            "High ridges mark the northern rim with clear views across the upland and distant slate hills beyond far.",
        ],
        [
            "Lodgepole pine borders the middle valley with sturdy trunks, brown bark, and layered branches around sheltered woodland.",
            "Conifer needles form a reddish carpet over moist acidic soil beside cedar groves and mossy clearings near the pasture.",
            "Wild ferns grow beneath leafy birch boughs near the meadow margin and grassy pasture beside the woodland.",
            "Purple heather flowers in spacious glades amid timber stands and fern-covered ground beneath the trees.",
            "Moss patches decorate birch roots beside secluded woodland glades and leafy undergrowth across the valley.",
        ],
        [
            "A gravel brook crosses the lowland between smooth pebbles, low plants, and overhanging shrubs under willows.",
            "Basalt pools gather beside low stone steps with reeds and sedges along the margins beside a wooded slope.",
            "Driftwood twigs lie on silted sandbars beside marsh grasses and yellow iris near the watercourse.",
            "River cobbles border the stream channel near wetland plants and a wooden footbridge with wooden rails.",
            "Soft sand lines the western bend beside a wooded slope and a shallow ford beneath green twigs nearby.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "31 hikers",
            "content": (
                "From the Redstone Ridge trail, 31 hikers were evacuated."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "trail ranger's notes written from a relayed message",
                "authority": "trail ranger",
                "quality": "weak",
                "why": "notes written by a trail ranger from a message relayed by a ranger positioned away from the trail",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "36 hikers",
            "content": (
                "Hikers evacuated from the Redstone Ridge trail numbered 36."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "trail ranger's notes written at the trailhead",
                "authority": "trail ranger",
                "quality": "strong",
                "why": "notes written by a trail ranger at the trailhead while each evacuated hiker was accounted for",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "36 hikers",
            "content": (
                "The Redstone Ridge trail saw 36 hikers evacuated."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "assembly-point medical notes",
                "authority": "medical personnel",
                "quality": "strong",
                "why": "medics at the assembly point examined every hiker evacuated from the trail, hurt or not, and entered each one in their own notes",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "36 hikers",
            "content": (
                "36 hikers were evacuated off the Redstone Ridge trail."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "shuttle drivers' evacuation notes",
                "authority": "transport driver",
                "quality": "strong",
                "why": "every hiker evacuated from the trail rode out on the shuttles, and the drivers listed each one by name in their own notes",
            },
        },
    },
}