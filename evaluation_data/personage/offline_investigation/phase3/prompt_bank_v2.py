"""
Phase 3 — E-improved prompt and exemplar bank.

Changes from v1:
  1. System prompt adds explicit low-E detection guards
  2. Exemplar set rebalanced: 4 low-E, 3 mid-E, 4 high-E (was 2 low / 9 high)
"""

TRAIT_FIRST_V2 = {
    "id": "trait_first_v2",
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
        "Extraversion calibration (critical):\n"
        "- Short, terse, or minimal utterances do NOT indicate high Extraversion — they often indicate LOW Extraversion.\n"
        "- Hedging ('I am not sure', 'I mean', 'you know') signals introversion, not energy.\n"
        "- Flat, withdrawn, or reluctant delivery = low E, even if the content is polite.\n"
        "- Reserve high E for genuinely energetic, assertive, socially dominant speech.\n"
        "- Use the full [-1, +1] range for E. Many speakers are introverted (E < 0).\n\n"
        "Return only valid JSON: {\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
    ),
}

# Rebalanced exemplar set: 4 low-E, 3 mid-E, 4 high-E
EXEMPLAR_IDS_V2 = [
    # Low E (4 exemplars)
    "open_low-compare2-Les_Routiers-Radio_Perfecto-7",          # E=-0.917, full OCEAN
    "random-compare2-Acacia-Marinella-15",                      # E=-0.750, full OCEAN
    "random-recommend-John_s_Pizzeria-12",                      # E=-0.750, full OCEAN
    "random-recommend-Pepolino-13",                             # E=-0.667, full OCEAN
    # Mid E (3 exemplars)
    "ems_low-recommend-Chimichurri_Grill-1",                    # E=+0.000
    "random-recommend-Cent_anni-10",                            # E=+0.083
    "random-compare2-Acacia-Marinella-11",                      # E=+0.167
    # High E (4 exemplars)
    "consc_high-compare2-Acacia-Marinella-6",                   # E=+0.667
    "agree_high-recommend-Chimichurri_Grill-4",                 # E=+0.750
    "open_high-compare2-Caffe_Cielo-Trattoria_Spaghetto-8",    # E=+0.833
    "random-recommend-Flor_De_Mayo-11",                         # E=+1.000
]

# Original v1 for comparison
TRAIT_FIRST_V1_ID = "trait_first"
EXEMPLAR_IDS_V1 = [
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
