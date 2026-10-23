"""M19: Evacuation clearing count during the fictional Redstone Ridge trail fire.

Incident status domain, directness quality dimension, tier T2.
"""

CASE = {
    "case_id": "M19",
    "domain": "incident_status",
    "question": "How many hikers were evacuated from the Redstone Ridge trail?",
    "world_truth": "36 hikers",
    "distractors": ["24 hikers", "48 hikers"],  # [24, 30, 36, 48] 
    "screen_partial": (
        "The number of hikers evacuated from the Redstone Ridge trail is between 27 and 39."
    ),  # keeps 30 and 36 (truth); rules out 24 and 48; both survivors sit 3 hikers inside bounds (R15)
    "quality_dimension": "directness",
    "difficulty_tier": "T2",
    "design_notes": (
        "Directness dimension, T2. A and B state the same proposition (the number of hikers evacuated "
        "from the Redstone Ridge trail) as flat, confident assertions with identical scope and no exceptions (R1). "
        "Both share the exact same five question content-words: hikers, evacuated, Redstone, Ridge, and trail (R13). "
        "Since this is a T2 case (control for dependence discounting without content cues), neither source "
        "carries an uncertainty hedge or adverbial modifier; both state their counts as flat assertions (R1, R16). "
        "Quality resides purely in provenance (R2, R19). Under Phase 4 directness rules, both writers hold "
        "identical individual standing as trail rangers, isolating directness: A is a relayed verbal message "
        "heard over radio from an off-site coordinator ('trail ranger relayed radio transmission'), while B is "
        "firsthand contemporaneous notes written at the trailhead perimeter ('trail ranger trailhead log notes') (R19). "
        "Neither type name contains 'independent', method indicators, or authority differences (R19). "
        "Sources B, C, and D state the truth using distinct syntactic frames to keep pairwise bigram overlap "
        "strictly below 0.40, satisfying A7 (R17). Options form a balanced spread [24, 30, 36, 48] hikers, "
        "with the truth (36) and A's claim (30) occupying interior positions (R8). The screen sentence uses "
        "two bounds (27 and 39), placing both survivors (30 and 36) exactly 3 hikers inside the bounds (R15). "
        "Content lengths are A=13 and B=13 words (|A - B| = 1 <= 2). Each filler set is exactly 79 words, "
        "landing long reports at 93 (Slot + A) and 92 (Slot + B) words, within the tight 91-93 band (R20). "
        "Fillers describe neutral physical geography and terrain (rock formations, forestry canopy, stream basin) "
        "with zero non-stopword content overlap across sets (R12), containing no numbers, dates, time markers, "
        "or fire incident vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "Exposed sandstone bluffs along the elevated plateau show prominent horizontal stratification bands across weathering rock faces.",
            "A natural scree slope descends towards the lower escarpment, carrying loose deposits of grey shale fragments.",
            "Cracked boulders rest beside the cliff boundary, supporting hardy colonies of lichens and small alpine mosses.",
            "Windblown dust settles across narrow fissures eroded into the limestone surface by dripping seasonal rainwater runoff.",
            "Steep jagged ridges outline the northern boundary horizon beneath bright unshaded morning skies arching overhead.",
        ],
        [
            "Dense stands of lodgepole pine border the middle valley basin where sheltered forest understorey continuously thrives.",
            "Fallen conifer needles create a thick reddish mulch over moist acidic soil beside timber woodland groves.",
            "Thick clusters of wild ferns spread beneath broad leafy birch boughs near the scenic meadow edge.",
            "Sunlight filters down through the canopy timber branches, illuminating vibrant patches of purple flowering woodland heather.",
            "Scattered green velvet cushions cling tightly to decayed birch roots near secluded shady forest clearings.",
        ],
        [
            "A flowing gravel brook winds quietly through the bottom ravine between smooth granite riverbed rounded pebbles.",
            "Clear spring water pools momentarily within carved basalt hollows before cascading over low tiered stone ledges.",
            "Waterlogged driftwood limbs lie grounded along silted gravel sandbanks fringed with tall marsh reeds and sedges.",
            "Washed river stones line the drainage channel margins where lush wetland grasses flourish along silt embankments.",
            "Fine wet sand covers the western stream bend where cool currents meet still coastal embayments.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "30 hikers",
            "content": (
                "Thirty hikers were evacuated from the Redstone Ridge trail during the emergency response."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "trail ranger relayed radio transmission",
                "authority": "trail ranger",
                "quality": "weak",
                "why": "secondhand verbal update heard over the vehicle radio from a ranger positioned away from the trail",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "36 hikers",
            "content": (
                "Hikers evacuated from the Redstone Ridge trail totalled thirty-six at the primary gate."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "trail ranger trailhead log notes",
                "authority": "trail ranger",
                "quality": "strong",
                "why": "firsthand tally recorded directly at the trailhead exit checkpoint as individuals were cleared",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "36 hikers",
            "content": (
                "Search coordinators cleared thirty-six hikers off the Redstone Ridge trail without injury."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "incident triage registry",
                "authority": "medical personnel",
                "quality": "strong",
                "why": "medical triage registry logging every person examined at the assembly clinic",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "36 hikers",
            "content": (
                "Thirty-six hikers arrived at the staging base from Redstone Ridge trail."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "transport shuttle roster",
                "authority": "transport driver",
                "quality": "strong",
                "why": "shuttle passenger roster signed by drivers transferring individuals from the scene",
            },
        },
    },
}