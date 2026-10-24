"""M20: Continuous runtime of the AeroGlide T5 vacuum cleaner on its standard power setting.

Product specifications domain, method quality dimension, tier T1.
"""

CASE = {
    "case_id": "M20",
    "domain": "product_spec",
    "question": (
        "What is the continuous runtime of the AeroGlide T5 vacuum cleaner "
        "on its standard power setting?"
    ),
    "world_truth": "48 minutes",
    "distractors": ["34 minutes", "55 minutes"],  # options: [34, 41, 48, 55], evenly spaced
    "screen_partial": (
        "The continuous runtime of the AeroGlide T5 vacuum cleaner on its standard power "
        "setting is between 37 minutes and 52 minutes."
    ),  # true, keeps 41 and 48 (truth), rules out 34 and 55; both survivors sit 4 minutes inside a bound (R15)
    "quality_dimension": "method",
    "difficulty_tier": "T1",
    "design_notes": (
        "Method dimension, T1. A and B state the same proposition (the continuous runtime of "
        "the AeroGlide T5 vacuum cleaner on its standard power setting) as single sentences "
        "with the same scope (R1). The question and all four sentences name the standard power "
        "setting, because a cordless vacuum's runtime is normally given per setting and a "
        "sentence that left it out could be read as a different mode, which would let 41 and "
        "48 both be true. Both A and B contain the same nine question content-words: "
        "continuous, runtime, AeroGlide, T5, vacuum, cleaner, standard, power and setting "
        "(R13). Neither copies the question's whole noun phrase: A is subject-first "
        "('The AeroGlide T5 vacuum cleaner is suspected to have a continuous runtime of ... at "
        "the standard power setting') and B is setting-fronted with the maker last ('With the "
        "standard power setting in use, the T5 vacuum cleaner from AeroGlide has ...'), so "
        "neither reads as the ready-made answer (R13). "
        "The T1 cue is A's clause-level hedge 'is suspected to' (R16), against B's flat "
        "assertion; M26 uses it too. It names no method, as a method case's hedge must not: "
        "'is estimated to' would state A's rough estimate in its sentence, and that belongs "
        "in its provenance (R2). "
        "Quality lives only in provenance (R2, R19) and only the method differs: both writers "
        "are testing technicians. A's type is a rough estimate from a short trial, whose why "
        "says a few minutes of use were timed and scaled up to a full battery, which can "
        "plausibly miss by several minutes; B's type is a timed trial to empty, whose why says "
        "the unit was run from a full charge until it stopped and the whole run was timed. "
        "Neither type name says who the writer is beyond 'technician', and neither contains "
        "'independent'. Type words are not subject words (R2a): no 'runtime', 'battery' or "
        "'vacuum'. 'Run' is left out of the type names because paraphrases of a runtime "
        "sentence may need it. "
        "Sources B, C and D each reach the figure by their own run (A7): B is a technician's "
        "timed trial, C is a consumer magazine's trial on a unit it bought from a shop, and D "
        "is a laboratory's trial on a different unit from a retail batch. None of the whys "
        "says one source copies another, and none rests on a declared or certified figure. C "
        "and D are plain statements of the same measure, the continuous runtime on the "
        "standard power setting, with digits for the number and 'vacuum cleaner' named, and "
        "they name no document, writer or method (R2, R6, R7). Frames differ (R17): B is "
        "setting-fronted, C says what the cleaner 'manages', and D is setting-fronted with "
        "'keeps going'. "
        "Options are 34, 41, 48 and 55 minutes: evenly spaced, none a round ten or a common "
        "advertised runtime, so a judge's sense of a normal figure does not lean either way, "
        "with the truth and A's claim both interior and equally far from the mean (R8). The "
        "screen sentence has two bounds, 37 and 52 minutes, and keeps 41 and 48 (each 4 "
        "minutes inside a bound) while ruling out 34 and 55 (R15). "
        "Content lengths are A=20 and B=20 words (R20). Each filler set is 72 words, so "
        "filler+A and filler+B are both 92, inside the 91-93 band. Filler is one plain fact "
        "per sentence about the look of three separate parts (the main body, the brush head "
        "and wand, the accessories): colour, material and shape only. It says nothing about "
        "power, charging, airflow, lighting or use, has no promotional wording, no time or "
        "process words, no damage words and no number words (R3, R9, R10). A script check "
        "found no word shared across two sets apart from articles and the most common "
        "function words (R12), and no word that occurs only in a source's provenance type "
        "(R2a)."
    ),

    "filler_sets": [
        [
            "The main body is moulded from matte grey resin with a smooth rounded outline.",
            "A silver band circles the middle of the body, and a small logo sits near the top.",
            "The front panel is curved and coloured in a slightly lighter shade of grey.",
            "A transparent bin sits in the front and shows its contents from all around.",
            "Slate feet at the base are round and slightly broader than the casing.",
        ],
        [
            "The brush head is flat and wide, with a black frame and a pale blue trim.",
            "Its bristles are stiff and cropped, arranged in strips across the underside.",
            "The wand is a long steel tube with a brushed finish and a collar at each end.",
            "Rubber wheels on either side of the head are white with yellow hubs.",
            "A hinged neck joins the head to the wand and is painted deep red.",
        ],
        [
            "The crevice nozzle is slender, made of orange nylon, and tapers to a pointed tip.",
            "A feather duster has soft cream feathers mounted on a wooden handle shaped like a paddle.",
            "The flexible hose is ribbed and green, and it is coiled in a loose spiral.",
            "A fabric storage bag is navy, zipped shut, with leather handles and a narrow strap.",
            "A beige strap of hook-and-loop tape holds the hose in place.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "41 minutes",
            "content": (
                "The AeroGlide T5 vacuum cleaner is suspected to have a continuous runtime "
                "of 41 minutes at the standard power setting."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "technician's rough estimate from a short trial",
                "authority": "testing technician",
                "quality": "weak",
                "why": "timed a few minutes of use on the standard power setting and scaled the result up to a full battery",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "48 minutes",
            "content": (
                "With the standard power setting in use, the T5 vacuum cleaner from AeroGlide "
                "has a continuous runtime of 48 minutes."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "technician's timed trial to empty",
                "authority": "testing technician",
                "quality": "strong",
                "why": "ran the vacuum cleaner on the standard power setting from a full charge until it stopped and timed the whole run",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "48 minutes",
            "content": (
                "The AeroGlide T5 vacuum cleaner manages 48 minutes of non-stop use on standard power."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "consumer magazine's timed trial",
                "authority": "consumer magazine",
                "quality": "strong",
                "why": "the magazine bought a unit from a shop, ran it on the standard power setting until it stopped and timed the whole run",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "48 minutes",
            "content": (
                "On its standard power setting, the AeroGlide T5 vacuum cleaner keeps going "
                "for 48 minutes at a stretch."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "laboratory's timed trial",
                "authority": "testing laboratory",
                "quality": "strong",
                "why": "a laboratory with no link to the maker took a different unit from a retail batch, ran it on the standard power setting until it stopped and timed the whole run",
            },
        },
    },
}