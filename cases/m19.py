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
        "Content lengths are A=9 and B=9 words (|A - B| = 0 <= 2). Filler sets are 82 to 84 words, "
        "landing long reports at 91 to 93 words, within the tight 91-93 band (R20). "
        "Filler describes the ridge's rock and plants, the meadows below it and the river in the valley, "
        "in plain one-fact sentences with no content word in two sets (R12). It leaves out steep or rough "
        "ground, paths, gathering places and people, which could bear on how hard an evacuation was (R9), "
        "and has no numbers, time or process words, or damage or age wording (R3, R10)."
    ),

    "filler_sets": [
        [
            "Redstone Ridge takes its name from its rust-coloured sandstone.",
            "Bands of pink and ochre run through the rock.",
            "Heather grows in purple drifts along the ridge.",
            "Gorse adds patches of bright yellow among the heather.",
            "Lichens in silver and pale green cover many of the boulders.",
            "Skylarks nest in the short grass on the crest.",
            "A cairn of piled rocks marks the highest point.",
            "From the cairn, the view stretches as far as the coast.",
            "Bilberry bushes grow in the hollows between the rocks.",
        ],
        [
            "Wildflower meadows lie at the foot of the ridge.",
            "Buttercups and clover fill the meadows from hedge to hedge.",
            "Common blue butterflies feed on knapweed and wild thyme.",
            "A family of hares lives near the hedgerows.",
            "Swallows skim low over the meadows by the stream.",
            "Barn owls roost in a broad oak beside the meadows.",
            "Orchids flower in the damp corners of the meadows.",
            "Moorhens raise their young among the rushes of a small pond.",
            "Bees hum among the foxgloves along the hedgerows.",
        ],
        [
            "The River Wend winds through the wide valley below the ridge.",
            "Alders and willows shade its muddy banks.",
            "A humpbacked bridge crosses the river beside a mill.",
            "The mill has a wooden wheel, a slate roof and a weathervane.",
            "Kingfishers dart from perches above the river.",
            "Trout hold in the deep pools under the arch of the bridge.",
            "Water crowfoot blooms white in the shallows.",
            "Otters have dens among the roots of the alders.",
            "Damselflies rest on the reeds by the bank.",
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