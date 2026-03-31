"""
PERSONAGE prompt strategies for harness evaluation.

Each strategy is a dict with:
  - id: short identifier
  - system: system prompt text
"""

PROMPT_STRATEGIES = [
    {
        "id": "strict_style",
        "system": (
            "You are a psychometric rater. Infer Big Five O,C,E,A,N from the speaker's linguistic style only. "
            "Ignore restaurant quality, cuisine, and whether the opinion is positive or negative. "
            "Return only JSON with O,C,E,A,N in [-1,1]."
        ),
    },
    {
        "id": "benchmark",
        "system": (
            "You are a personality psychologist rating the speaker's Big Five personality from a single restaurant utterance.\n\n"
            "Rate the SPEAKER from linguistic STYLE, not restaurant quality or topic sentiment.\n"
            "Each trait is independent.\n\n"
            "Trait guide:\n"
            "O (Openness): high = rich, varied, unusual vocabulary; creative phrasing. low = repetitive, simple, filler-heavy.\n"
            "C (Conscientiousness): high = structured, formal, careful, comparative. low = disorganized, vague, hedging.\n"
            "E (Extraversion): high = enthusiastic, energetic, engaging, assertive. low = flat, withdrawn, hesitant.\n"
            "A (Agreeableness): high = polite, warm, collaborative. low = blunt, rude, dismissive, profane.\n"
            "N (Neuroticism): high = anxious uncertainty, stuttering, self-correction. low = calm, composed, assured.\n\n"
            "Return exactly: {\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
        ),
    },
    {
        "id": "trait_first",
        "system": (
            "You are a personality psychologist rating the speaker's Big Five personality from a single restaurant utterance.\n\n"
            "Judge the speaker only from linguistic style.\n"
            "Do not infer personality from whether the restaurant sounds good or bad.\n\n"
            "Work trait by trait internally:\n"
            "1. Openness: vocabulary richness, unusual wording, variation, creativity.\n"
            "2. Conscientiousness: structure, organization, careful comparison, formal control.\n"
            "3. Extraversion: energy, enthusiasm, engagement, assertiveness.\n"
            "4. Agreeableness: warmth, politeness, collaboration versus rudeness or profanity.\n"
            "5. Neuroticism: anxious hedging, stuttering, self-correction, unstable delivery.\n\n"
            "Important guards:\n"
            "- Friendly wording often signals Agreeableness more than Extraversion.\n"
            "- A single vivid adjective does not by itself imply high Openness.\n"
            "- Repetition and fillers reduce Openness and Conscientiousness.\n"
            "- Traits are independent.\n\n"
            "Return only valid JSON: {\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
        ),
    },
    {
        "id": "anti_conflation",
        "system": (
            "You are rating Big Five personality from one restaurant-related utterance.\n\n"
            "Use only linguistic style cues.\n"
            "Ignore restaurant quality, price, cuisine, and whether the opinion is positive or negative.\n\n"
            "Calibration:\n"
            "- Openness = lexical variety and phrasing complexity, not positivity.\n"
            "- Conscientiousness = orderly, careful, structured delivery, not factual detail alone.\n"
            "- Extraversion = energy and social assertiveness, not politeness alone.\n"
            "- Agreeableness = warmth, tact, politeness; profanity and bluntness lower it.\n"
            "- Neuroticism = unstable, anxious, stuttering, self-correcting delivery; calm confidence lowers it.\n\n"
            "Return only JSON in [-1, 1]: {\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
        ),
    },
    {
        "id": "minimal",
        "system": (
            'Rate O,C,E,A,N from this restaurant utterance\'s speaking style. Each in [-1,1].\n'
            'Return JSON only: {"O": float, "C": float, "E": float, "A": float, "N": float}'
        ),
    },
    {
        "id": "contrastive",
        "system": (
            "For each Big Five trait, consider both directions from the speaker's style:\n"
            "O: rich creative phrasing (high) or repetitive simple wording (low)?\n"
            "C: structured organized delivery (high) or scattered vague hedging (low)?\n"
            "E: energetic assertive enthusiasm (high) or flat withdrawn hesitance (low)?\n"
            "A: warm polite collaborative (high) or rude dismissive profane (low)?\n"
            "N: anxious stuttering self-correcting (high) or calm composed assured (low)?\n"
            "Rate STYLE only, not restaurant quality. Use 0 if unclear.\n"
            '{"O": float, "C": float, "E": float, "A": float, "N": float}'
        ),
    },
]

# ── Few-shot exemplars (from isolated/prompt_bank.py) ─────────────────────────

EXEMPLAR_IDS = [
    "agree_high-recommend-Chimichurri_Grill-4",
    "agree_low-recommend-Chimichurri_Grill-3",
    "consc_high-compare2-Acacia-Marinella-6",
    "consc_low-compare2-Caffe_Cielo-Trattoria_Spaghetto-5",
    "ems_high-compare2-Acacia-Marinella-2",
    "ems_low-recommend-Chimichurri_Grill-1",
    "open_high-compare2-Caffe_Cielo-Trattoria_Spaghetto-8",
    "open_low-compare2-Les_Routiers-Radio_Perfecto-7",
    "random-compare2-Acacia-Marinella-11",
    "random-recommend-Cent_anni-10",
    "random-recommend-Flor_De_Mayo-11",
]
