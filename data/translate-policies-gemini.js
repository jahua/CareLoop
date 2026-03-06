#!/usr/bin/env node
/**
 * Translate policy documents from German/French to English using Google Gemini API.
 *
 * Input:  data/documents/cantonal/parsed_cantonal_policies.json
 * Output: data/documents/translated/translated_policies.json
 *
 * Usage:
 *   GEMINI_API_KEY=<your-key> node scripts/translate-policies-gemini.js
 *
 * Options:
 *   --dry-run       Show what would be translated without calling the API
 *   --single <id>   Translate only one document by source_id
 *   --delay <ms>    Delay between API calls (default: 1500ms for free tier)
 */

const fs = require("fs");
const path = require("path");
const https = require("https");

const API_KEY = process.env.GEMINI_API_KEY;
const MODEL = process.env.GEMINI_MODEL || "gemini-2.0-flash";
const INPUT_PATH =
  process.env.TRANSLATE_INPUT ||
  path.resolve(__dirname, "../data/documents/cantonal/parsed_cantonal_policies.json");
const OUTPUT_PATH =
  process.env.TRANSLATE_OUTPUT ||
  path.resolve(__dirname, "../data/documents/translated/translated_policies.json");
const DELAY_MS = Number(process.env.TRANSLATE_DELAY_MS || getArg("--delay") || "1500");

const DRY_RUN = process.argv.includes("--dry-run");
const SINGLE_ID = getArg("--single");

function getArg(flag) {
  const idx = process.argv.indexOf(flag);
  return idx !== -1 && process.argv[idx + 1] ? process.argv[idx + 1] : null;
}

const SYSTEM_PROMPT = `You are a professional translator specializing in Swiss social insurance and disability policy.

TASK: Translate the following document to English.

RULES — follow these strictly:
1. Preserve all markdown formatting (headings, lists, bold, links).
2. Keep Swiss-specific legal/insurance terms in parentheses after the English term.
   Examples:
   - "disability insurance (Invalidenversicherung / IV)"
   - "supplementary benefits (Ergänzungsleistungen / EL)"
   - "helplessness allowance (Hilflosenentschädigung / HE)"
   - "assistance contribution (Assistenzbeitrag)"
   - "vocational rehabilitation (berufliche Eingliederung)"
   - "daily allowance (Taggeld)"
   - "pension (Rente)"
   - "degree of disability (Invaliditätsgrad)"
   For French equivalents use the same pattern:
   - "disability insurance (assurance-invalidité / AI)"
   - "supplementary benefits (prestations complémentaires / PC)"
   - "helplessness allowance (allocation pour impotent)"
3. Do NOT translate: proper nouns (SVA Zürich, OCAS, IV-Stelle Kanton Bern), URLs, form numbers, addresses, phone numbers, email addresses.
4. Preserve the metadata header lines at the top (lines starting with #). Update only the language field to "en" and add "(translated from de/fr)".
5. Translate accurately — do not add, remove, or summarize information.
6. Use clear, accessible English suitable for caregivers and patients navigating the Swiss system.
7. Return ONLY the translated text, no preamble or explanation.`;

function callGemini(content, sourceLanguage) {
  return new Promise((resolve, reject) => {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;
    const body = JSON.stringify({
      contents: [
        {
          role: "user",
          parts: [
            {
              text: `${SYSTEM_PROMPT}\n\nSource language: ${sourceLanguage}\n\n---\n\n${content}`,
            },
          ],
        },
      ],
      generationConfig: {
        temperature: 0.1,
        maxOutputTokens: 8192,
      },
    });

    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            reject(new Error(`Gemini API error: ${json.error.message}`));
            return;
          }
          const text =
            json.candidates?.[0]?.content?.parts?.[0]?.text || "";
          resolve(text.trim());
        } catch (e) {
          reject(new Error(`Failed to parse Gemini response: ${e.message}`));
        }
      });
    });

    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function run() {
  if (!DRY_RUN && !API_KEY) {
    console.error("ERROR: GEMINI_API_KEY environment variable is required.");
    console.error("Get a free key at: https://aistudio.google.com/apikey");
    process.exit(1);
  }

  if (!fs.existsSync(INPUT_PATH)) {
    console.error(`Input file not found: ${INPUT_PATH}`);
    process.exit(1);
  }

  const documents = JSON.parse(fs.readFileSync(INPUT_PATH, "utf8"));
  if (!Array.isArray(documents) || documents.length === 0) {
    console.error("Input must be a non-empty JSON array.");
    process.exit(1);
  }

  let existing = [];
  if (fs.existsSync(OUTPUT_PATH)) {
    try {
      existing = JSON.parse(fs.readFileSync(OUTPUT_PATH, "utf8"));
    } catch (_) {
      existing = [];
    }
  }
  const doneIds = new Set(existing.map((d) => d.source_id));

  const toTranslate = documents.filter((doc) => {
    if (SINGLE_ID) return doc.source_id === SINGLE_ID;
    if (doc.metadata?.language === "en") return false;
    return !doneIds.has(doc.source_id);
  });

  console.log(`\n=== CareLoop Policy Translation ===`);
  console.log(`Input:    ${INPUT_PATH}`);
  console.log(`Output:   ${OUTPUT_PATH}`);
  console.log(`Model:    ${MODEL}`);
  console.log(`Total documents:     ${documents.length}`);
  console.log(`Already translated:  ${doneIds.size}`);
  console.log(`To translate:        ${toTranslate.length}`);
  console.log(`Delay between calls: ${DELAY_MS}ms`);
  if (DRY_RUN) console.log(`MODE: DRY RUN (no API calls)\n`);
  else console.log();

  if (toTranslate.length === 0) {
    console.log("Nothing to translate. All documents are done.");
    return;
  }

  for (const doc of toTranslate) {
    const lang = doc.metadata?.language || "de";
    const langName = lang === "fr" ? "French" : "German";
    console.log(
      `[${toTranslate.indexOf(doc) + 1}/${toTranslate.length}] ` +
        `Translating ${doc.source_id} (${langName}, ${doc.content.length} chars)...`
    );

    if (DRY_RUN) {
      console.log(`  → Would translate: "${doc.title}" (${langName} → English)`);
      continue;
    }

    try {
      const translated = await callGemini(doc.content, langName);

      const result = {
        source_id: doc.source_id,
        title: doc.title,
        title_en: null,
        url: doc.url,
        content_original: doc.content,
        content_en: translated,
        metadata: {
          ...doc.metadata,
          language_original: lang,
          language: "en",
          translated_at: new Date().toISOString(),
          translated_model: MODEL,
        },
      };

      const titleMatch = translated.match(/^#\s+(.+?)(?:\n|$)/m);
      if (titleMatch) {
        result.title_en = titleMatch[1].replace(/\s*—.*$/, "").trim();
      }

      existing.push(result);

      fs.writeFileSync(OUTPUT_PATH, JSON.stringify(existing, null, 2), "utf8");

      console.log(
        `  ✓ Done (${translated.length} chars). ` +
          (result.title_en ? `English title: "${result.title_en}"` : "")
      );

      if (toTranslate.indexOf(doc) < toTranslate.length - 1) {
        await sleep(DELAY_MS);
      }
    } catch (err) {
      console.error(`  ✗ FAILED: ${err.message}`);
      console.error(`  → Skipping ${doc.source_id}. Re-run to retry.`);
    }
  }

  console.log(`\n=== Translation complete ===`);
  console.log(`Output written to: ${OUTPUT_PATH}`);
  console.log(`Total translated: ${existing.length}/${documents.length}`);
}

run().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
