"""M17: Package holding limit at the Highfield Parcel Centre.

Institutional logistics domain, directness quality dimension, tier T1.
"""

CASE = {
    "case_id": "M17",
    "domain": "institutional_logistics",
    "question": "What is the package holding limit at Highfield Parcel Centre?",
    "world_truth": "21 days",
    "distractors": ["7 days", "28 days"],  #[7, 14, 21, 28]
    "screen_partial": (
        "The package holding limit at Highfield Parcel Centre is between 10 days and 25 days."
    ),  # keeps 14 and 21 (truth); rules out 7 and 28; both survivors sit 4 days inside bounds (R15)
    "quality_dimension": "directness",
    "difficulty_tier": "T1",
    "design_notes": (
        "Directness dimension, T1. A and B state the same proposition (the package holding "
        "limit at Highfield Parcel Centre) as single sentences with identical scope (R1). "
        "Both contain the exact same six question content-words: package, holding, limit, "
        "Highfield, Parcel, and Centre (R13). The T1 cue is A's clause-level hedge "
        "'is expected to be' (R16), which survives faithful paraphrasing while varying from "
        "cues used in earlier cases ('is understood to', 'is believed to', 'is presumed to', "
        "'is considered to'). Quality resides strictly in provenance (R2, R19). Under Phase 4 "
        "directness rules, both writers have the same individual standing as logistics couriers, "
        "isolating directness: A relies on second-hand information passed on by a driver who was "
        "not at the depot, whereas B relies on first-hand notes written at the intake counter itself (R19). "
        "Neither type name leaks methodology, authority differences, or the word 'independent' (R19). "
        "Sources B, C, and D state the truth using distinct syntactic frames to keep bigram overlap "
        "below 0.40 (R17). Distractors form a balanced spread [7, 14, 21, 28], with the truth (21) and "
        "A's claim (14) occupying the interior positions (R8). The screen sentence uses two bounds "
        "(10 and 25 days), placing both survivors (14 and 21) exactly 4 days inside the bounds (R15). "
        "Content lengths are A=14, & B=14 words. Each filler set is 77-79 words, "
        "landing every long report is within the tight 91-93 band (R20). Fillers describe "
        "neutral physical warehouse environments across three separate zones (loading apron, dispatch "
        "foyer, vehicle yard) without cross-set noun sharing (R12), and contain no numbers, time markers, "
        "prohibited words, or package holding vocabulary (R3, R9, R10)."
    ),

    "filler_sets": [
        [
            "The concrete loading apron has yellow perimeter lines painted along the outer raised vehicle docking bays.",
            "A steel roller shutter stays locked down above the central machinery ramp when outside working shifts.",
            "Heavy rubber buffers mounted beside the bay openings cushion delivery lorries during reversing manoeuvres across bays.",
            "Overhead halogen floodlights illuminate the external tarmac expanse through wide protective lenses mounted on tall masts.",
            "Galvanised drainage grilles stretch across the lower perimeter trench to channel heavy storm water away.",
        ],
        [
            "The front customer foyer contains broad timber benches situated beneath fixed aluminium framed wall information vitrines.",
            "Polished terrazzo floor tiles run between the double glass entry partitions and the reception counter.",
            "Recessed ceiling downlights provide continuous warm illumination above the visitor queuing barrier lanes during daytime access.",
            "A decorative indoor planter filled with glossy broadleaf shrubs separates the waiting area from doorways.",
            "Low acoustic ceiling baffles absorb background mechanical hum within the public intake hall without distraction.",
        ],
        [
            "The staff parking enclosure is bordered by high wire chainlink fencing topped with metal barbed coils.",
            "Precast stone edging blocks separate designated car spaces from the primary transit lorry access trackway.",
            "A marked pedestrian walkway guides guests from the outer gatehouse toward the administration building annex.",
            "Reflective directional signage boards attached to boundary stanchions indicate designated turning routes around the campus loop.",
            "Neat gravel strips run beside the security gatehouse to prevent rainwater puddles forming along pathways.",
        ],
    ],

    "sources": {
        "A": {
            "quality": "weak",
            "claim": "14 days",
            "content": (
                "The package holding limit at Highfield Parcel Centre is expected to be 14 days."
            ),
            "n_paraphrases_needed": 2,
            "provenance": {
                "type": "summary passed on by a courier who missed the intake briefing",
                "authority": "individual",
                "quality": "weak",
                "why": "second-hand information heard from another driver rather than directly recorded during the depot briefing",
            },
        },
        "B": {
            "quality": "strong",
            "claim": "21 days",
            "content": (
                "Packages at Highfield Parcel Centre are stored for a holding limit of 21 days."
            ),
            "n_paraphrases_needed": 3,
            "provenance": {
                "type": "notes taken at the intake desk by a courier at the briefing",
                "authority": "individual",
                "quality": "strong",
                "why": "first-hand notes recorded contemporaneously on site during the parcel centre's intake briefing",
            },
        },
        "C": {
            "quality": "strong",
            "claim": "21 days",
            "content": (
                "Highfield Parcel Centre holds incoming packages for twenty-one days before return processing."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "intake counter logbook",
                "authority": "depot clerk",
                "quality": "strong",
                "why": "intake log entries stamped at the delivery counter establishing physical custody duration",
            },
        },
        "D": {
            "quality": "strong",
            "claim": "21 days",
            "content": (
                "Twenty-one days represents the storage duration permitted for consignments at Highfield Parcel Centre."
            ),
            "n_paraphrases_needed": 1,
            "provenance": {
                "type": "depot dispatch register",
                "authority": "depot clerk",
                "quality": "strong",
                "why": "daily dispatch register detailing holding capacity thresholds for uncollected parcels",
            },
        },
    },
}