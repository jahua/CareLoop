# How to Translate Policy Documents Using Gemini

Step-by-step guide to translate all German/French policy documents to English for Big5Loop RAG retrieval.

---

## Prerequisites

1. **Node.js** (already installed)
2. **A Google Gemini API key** (free)

---

## Step 1: Get a Gemini API Key (free, 2 minutes)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API key"**
4. Copy the key (starts with `AIza...`)

Free tier limits (more than enough for 21 documents):
- 15 requests per minute
- 1 million tokens per minute
- 1500 requests per day

## Step 2: Add the key to your `.env`

```bash
cd Big5Loop

# Add to .env (do NOT commit this)
echo "" >> .env
echo "# Google Gemini API (translation + future embeddings)" >> .env
echo "GEMINI_API_KEY=your-key-here" >> .env
```

Replace `your-key-here` with the actual key.

## Step 3: Preview what will be translated (dry run)

```bash
cd Big5Loop
node scripts/translate-policies-gemini.js --dry-run
```

Expected output:
```
=== Big5Loop Policy Translation ===
Total documents:     21
Already translated:  0
To translate:        21
MODE: DRY RUN (no API calls)

[1/21] Translating zh_iv_rente (German, 1842 chars)...
  → Would translate: "Zürich – IV-Rente (SVA Zürich)" (German → English)
[2/21] Translating zh_iv_hilflosenentschaedigung (German, 1654 chars)...
...
```

## Step 4: Run the translation

```bash
cd Big5Loop

# Load the API key
source .env
# or: export GEMINI_API_KEY=your-key-here

# Run translation
GEMINI_API_KEY=$GEMINI_API_KEY node scripts/translate-policies-gemini.js
```

This will:
- Call Gemini API once per document (21 calls total)
- Wait 1.5 seconds between calls (respects free tier rate limit)
- Save progress after each document (safe to interrupt and resume)
- Write output to `data/documents/translated/translated_policies.json`

**Estimated time:** ~45 seconds (21 docs × ~1.5s delay + API latency)

**Estimated cost:** $0.00 (well within free tier)

### Options

```bash
# Translate a single document (for testing)
GEMINI_API_KEY=... node scripts/translate-policies-gemini.js --single zh_iv_rente

# Use a different model
GEMINI_MODEL=gemini-2.0-flash GEMINI_API_KEY=... node scripts/translate-policies-gemini.js

# Adjust delay between calls (default 1500ms)
GEMINI_API_KEY=... node scripts/translate-policies-gemini.js --delay 2000
```

## Step 5: Review the translations

Open the output file and spot-check a few:

```bash
# Quick look at the output
cat data/documents/translated/translated_policies.json | head -50

# Check how many were translated
node -e "console.log(JSON.parse(require('fs').readFileSync('data/documents/translated/translated_policies.json','utf8')).length)"
```

Key things to verify:
- [ ] Swiss terms are preserved in parentheses: "disability insurance (Invalidenversicherung / IV)"
- [ ] URLs, addresses, phone numbers are NOT translated
- [ ] Markdown structure is preserved
- [ ] No information added or removed

## Step 6: Load English chunks into the database

```bash
cd Big5Loop

# Make sure PostgreSQL is running
docker compose up -d postgres

# Load translated chunks
DATABASE_URL=postgresql://big5loop:changeme@localhost:5432/big5loop \
  node scripts/load-translated-policies.js
```

This creates English chunks alongside the originals:
- Original: `source_id = zh_iv_rente` (German)
- English:  `source_id = zh_iv_rente_en` (English translation)

## Step 7: Update the retrieval query (workflow)

The current workflow query searches using English FTS against German content (broken). After loading English chunks, the query will naturally find them because:

- `to_tsvector('english', content)` correctly indexes English content
- `websearch_to_tsquery('english', user_message)` correctly parses English queries
- Keyword overlap now works: "eligible" matches "eligible" in the English chunk

**No workflow change needed** — the existing FTS query will automatically pick up the English chunks.

Optional improvement: prefer English chunks in retrieval by adding a filter:

```sql
-- In the workflow retrieval query, add to prefer English chunks:
AND (metadata->>'language' = 'en' OR metadata->>'language' IS NULL)
```

## Step 8: Verify end-to-end

```bash
# Check chunks in database
docker exec -i big5loop-postgres psql -U big5loop -d big5loop -c \
  "SELECT source_id, title, length(content), metadata->>'language' as lang FROM policy_chunks ORDER BY source_id;"

# Count by language
docker exec -i big5loop-postgres psql -U big5loop -d big5loop -c \
  "SELECT metadata->>'language' as lang, count(*) FROM policy_chunks GROUP BY 1;"
```

Expected: you should see both original (de/fr) and translated (en) chunks.

---

## Re-running after source updates

If you re-crawl or update source documents:

1. Re-run the translation script — it skips already-translated documents
2. To force re-translate a specific document:

```bash
# Delete from output, then re-run
GEMINI_API_KEY=... node scripts/translate-policies-gemini.js --single zh_iv_rente
```

3. Re-load into database:

```bash
DATABASE_URL=... node scripts/load-translated-policies.js
```

---

## Files created by this process

| File | Purpose |
|------|---------|
| `scripts/translate-policies-gemini.js` | Translation script (Gemini API) |
| `scripts/load-translated-policies.js` | Load English chunks into DB |
| `data/documents/translated/translated_policies.json` | Translation output (all 21 docs) |
| `data/documents/TRANSLATION-INVENTORY.md` | Document inventory and status |
| `data/documents/TRANSLATION-INSTRUCTIONS.md` | This file |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `GEMINI_API_KEY is required` | Set the env var: `export GEMINI_API_KEY=AIza...` |
| `429 Too Many Requests` | Increase delay: `--delay 3000` |
| `Gemini API error: quota exceeded` | Wait a minute (free tier: 15 req/min) |
| Translation stops mid-way | Just re-run — it resumes from where it left off |
| Bad translation quality | Try `GEMINI_MODEL=gemini-2.5-flash` for better quality |
| Script hangs | Check internet connection; Ctrl+C and re-run |
