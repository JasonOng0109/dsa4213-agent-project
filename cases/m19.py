"""M19: Evacuation clearing count during the Redstone Ridge trail fire.

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
        "with zero non-stopword content overlap across sets (R12), containing no numbers, dates, time markers, "
        "or fire incident vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "Exposed sandstone bluffs along the elevated plateau show prominent horizontal stratification bands across weathering rock faces above a shadowed ravine with broken terraces and pale ledges.",
            "A natural scree slope descends towards the escarpment, carrying loose deposits of grey shale fragments.",
            "Cracked boulders rest beside the cliff boundary, supporting hardy colonies of lichens and alpine mosses.",
            "Windblown dust settles across narrow fissures eroded into the limestone surface by rainwater runoff.",
            "Steep jagged crags of quartzite rise along the northern rim of the plateau.",
        ],
        [
            "Dense stands of lodgepole pine border the middle valley basin where sheltered forest understorey thrives with tall trunks, dark bark, and layered branches around the basin.",
            "Fallen conifer needles create a thick reddish mulch over moist acidic soil beside woodland groves.",
            "Thick clusters of wild ferns spread beneath broad leafy birch boughs near the meadow edge.",
            "Purple heather flowers in open glades amid the timber stands and fern-covered ground.",
            "Scattered green velvet cushions cling tightly to decayed birch roots near secluded forest hollows.",
        ],
        [
            "A gravel brook winds through the bottom ravine between smooth granite pebbles and dark banks under overhanging shrubs and beside moss-covered banks along a narrow channel.",
            "Spring water gathers within carved basalt hollows before cascading over low tiered stone ledges.",
            "Waterlogged driftwood limbs lie along silted sandbanks fringed with tall marsh reeds and sedges.",
            "Washed river stones line the channel margins where lush wetland grasses flourish beside embankments.",
            "Fine wet sand covers the western bend where cool currents pass beneath a wooded ravine.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "30 hikers",
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