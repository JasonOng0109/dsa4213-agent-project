"""M7: Rated brightness of the fictional LumaDesk S3 desk lamp.

Product specifications, authority quality dimension, tier T1.
Tests conflicting brightness ratings from sources of differing authority.
"""

CASE = {
    "case_id": "M7",
    "domain": "product_spec",
    "question": "What is the rated brightness of the LumaDesk S3 desk lamp?",
    "world_truth": "600 lm",
    "distractors": ["400 lm", "700 lm"],
    "screen_partial": (
        "The LumaDesk S3 desk lamp has a rated brightness "
        "greater than 400 lm and less than 700 lm."
    ),
    "quality_dimension": "authority",
    "difficulty_tier": "T1",
    "design_notes": (
        "This case tests the authority quality dimension using conflicting "
        "brightness ratings for the fictional LumaDesk S3 desk lamp. "
        "Source A is an informal product-review website claiming 500 lm, "
        "while Source B is an accredited lighting performance authority "
        "supporting the true value of 600 lm. "
        "A is weaker because the reviewer lacks recognised authority to "
        "establish the lamp's rated brightness, whereas B has recognised "
        "expertise in lighting performance (R19). "
        "A and B describe the same product and brightness rating, using "
        "equally specific claims with no exceptions or changes (R1). "
        "Both retain the relevant question terms identifying the lamp "
        "and its brightness (R13). "
        "Source A contains the mild clause-level hedge 'is believed to have', "
        "which is intended to survive reporter paraphrasing (R16). "
        "The T1 classification remains provisional until the frozen reports "
        "are checked; if the hedge disappears, the case becomes T2. "
        "Source identity, authority and assessment methods are kept in "
        "provenance rather than content (R2). "
        "Sources B, C and D use distinct sentence structures while "
        "supporting the same brightness value (R17). "
        "Their independence must be checked to ensure that A7 represents "
        "three independent sources rather than repeated evidence. "
        "The four options are 400, 500, 600 and 700 lm, with both competing "
        "claims occupying the interior positions (R8). "
        "The screening sentence preserves 500 and 600 lm while excluding "
        "400 and 700 lm, retaining the world truth (R15). "
        "The three filler sets describe neutral physical features of the "
        "lamp without mentioning brightness, electrical performance or "
        "source-identifying language (R9, R10). "
        "The filler lengths and source sentence lengths have been checked "
        "against the required long-report range, with no R20 warnings."
    ),
    # Filler belongs to the SLOT, not the source (R12): one set per report position, so
    # two reports of the shared source never carry identical padding.
    "filler_sets": [
        [
            "The LumaDesk S3 desk lamp has a circular base with a matte finish and rounded edges.",
            "A slender stem rises from the base and curves toward a broad shade with a surface.",
            "The shade has a shallow dome shape, and its rim follows a smooth line around the opening.",
            "A joint connects the shade to the stem, allowing the head to tilt in different directions.",
            "The base rests flat on a desk, with a pad covering its underside.",
        ],
        [
            "The LumaDesk S3 desk lamp stands on a compact base with a slightly textured surface.",
            "Its upright stem has a narrow profile and meets the shade through a discreet adjustable joint.",
            "The shade is shaped like a shallow bowl, with a smooth rim and a curved exterior.",
            "A small control button sits near the base, flush with the surrounding surface.",
            "The stem and shade share a consistent finish, while the underside of the base has a protective lining.",
        ],
        [
            "The LumaDesk S3 desk lamp features a circular base and a gently angled supporting stem.",
            "The shade has a rounded outline with a smooth exterior and a finished edge.",
            "A hinged connection joins the shade to the stem, letting the head move without shifting the base.",
            "The control surface is plain, with a small button set into the top of the base.",
            "A pad beneath the base helps protect the desk, and the stem has no visible decoration.",
        ],
    ],
    "sources": {
        "A": {
            "quality": "weak",
            "claim": "500 lm",
           "content": (
                "The LumaDesk S3 desk lamp is believed to have "
                "a rated brightness of 500 lm."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "informal product-review website",
                "authority": "Independent hobbyist reviewer",
                "quality": "weak",
                "why": (
                    "The reviewer has no recognised authority to "
                    "establish the lamp's rated brightness."
                ),
            },
        },
        "B": {
            "quality": "strong",
            "claim": "600 lm",
            "content": (
                "A rated brightness of 600 lm applies to "
                "the LumaDesk S3 desk lamp model."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "accredited lighting performance authority",
                "authority": "Recognised lighting standards body",
                "quality": "strong",
                "why": (
                    "The body has recognised expertise and authority "
                    "in evaluating lighting performance."
                ),
            },
        },
        "C": {
            "quality": "strong",
            "claim": "600 lm",
            "content": (
                "The LumaDesk S3 desk lamp produces "
                "a brightness of 600 lm."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "independent lighting assessment body",
                "authority": "Accredited lighting assessment organisation",
                "quality": "strong",
                "why": (
                    "The organisation independently evaluates lighting "
                    "performance using its own assessment process."
                ),
            },
        },
        "D": {
            "quality": "strong",
            "claim": "600 lm",
            "content": (
                "For the LumaDesk S3 desk lamp, "
                "600 lm is its rated brightness."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "accredited lighting compliance assessor",
                "authority": "Recognised lighting compliance organisation",
                "quality": "strong",
                "why": (
                    "The assessor independently evaluates the lamp's "
                    "brightness without relying on the other reports."
                ),
            },
        },
    },
}
