from __future__ import annotations

from pathlib import Path
import json


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


BENCHMARK_SYSTEM = (
    "You are a personality psychologist rating the speaker's Big Five personality from a single restaurant utterance.\n\n"
    "Rate the SPEAKER from linguistic STYLE, not restaurant quality or topic sentiment.\n"
    "Each trait is independent.\n\n"
    "Trait guide:\n"
    "O (Openness): high = rich, varied, or unusual vocabulary; creative phrasing sustained across the utterance. "
    "low = repetitive, simple, filler-heavy wording. Do NOT rate O high from a single adjective like 'nice' or 'good'.\n"
    "C (Conscientiousness): high = structured, formal, careful, comparative, organized phrasing. "
    "low = disorganized, vague, repetitive, hedging, scattered delivery.\n"
    "E (Extraversion): high = enthusiastic, energetic, engaging, assertive, lively. "
    "low = flat, withdrawn, hesitant, low-energy, minimal. Do NOT rate E high just because the speaker is polite or says 'you would like it'.\n"
    "A (Agreeableness): high = polite, warm, collaborative, accommodating. "
    "low = blunt, rude, dismissive, profane, harsh.\n"
    "N (Neuroticism): high = anxious uncertainty, stuttering, self-correction, unstable delivery, distressed hedging. "
    "low = calm, composed, assured, steady delivery.\n\n"
    "Important calibration rules:\n"
    "- Rate STYLE, not whether the restaurant is good or bad.\n"
    "- A speaker can be high in A and low in N at the same time.\n"
    "- A short positive recommendation can still be low or moderate O and E.\n"
    "- Friendly recommendation language often signals A more than E.\n"
    "- Repetition, fillers, and broken delivery reduce O and C even when the speaker sounds positive.\n"
    "- Use the full range [-1.0, 1.0] when the evidence is strong.\n"
    "- Return only valid JSON.\n\n"
    "Return exactly:\n"
    "{\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
)

TRAIT_FIRST_SYSTEM = (
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
    "- Calm short recommendations can still be low Extraversion.\n"
    "- Repetition and fillers reduce Openness and Conscientiousness.\n"
    "- Traits are independent.\n\n"
    "Return only valid JSON:\n"
    "{\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
)

ANTI_CONFLATION_SYSTEM = (
    "You are rating Big Five personality from one restaurant-related utterance.\n\n"
    "Use only linguistic style cues.\n"
    "Ignore restaurant quality, price, cuisine, and whether the opinion is positive or negative.\n\n"
    "Calibration:\n"
    "- Openness = lexical variety and phrasing complexity, not positivity.\n"
    "- Conscientiousness = orderly, careful, structured delivery, not factual detail alone.\n"
    "- Extraversion = energy and social assertiveness, not politeness alone.\n"
    "- Agreeableness = warmth, tact, politeness; profanity and bluntness lower it.\n"
    "- Neuroticism = unstable, anxious, stuttering, self-correcting delivery; calm confidence lowers it.\n\n"
    "Return only JSON in [-1, 1]:\n"
    "{\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
)

SYSTEM_PROMPTS = {
    "benchmark": BENCHMARK_SYSTEM,
    "trait_first": TRAIT_FIRST_SYSTEM,
    "anti_conflation": ANTI_CONFLATION_SYSTEM,
}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_fewshot_messages(dataset_rows: list[dict], variant: str = "benchmark") -> list[dict]:
    rows_by_id = {row["id"]: row for row in dataset_rows}
    missing = [row_id for row_id in EXEMPLAR_IDS if row_id not in rows_by_id]
    if missing:
        raise ValueError(f"Missing exemplar ids in dataset: {missing}")

    if variant not in SYSTEM_PROMPTS:
        raise ValueError(f"Unknown prompt variant: {variant}")

    messages = [{"role": "system", "content": SYSTEM_PROMPTS[variant]}]
    for row_id in EXEMPLAR_IDS:
        row = rows_by_id[row_id]
        messages.append({"role": "user", "content": f'Utterance: "{row["input"]}"'})
        messages.append(
            {
                "role": "assistant",
                "content": json.dumps(row["ground_truth_ocean"], ensure_ascii=False),
            }
        )
    return messages
