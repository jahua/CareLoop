const { Client } = require('pg');

const client = new Client({
  connectionString: process.env.DATABASE_URL || 'postgresql://big5loop:changeme@localhost:5432/big5loop',
});

const SCHEMA_SQL = `
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS policy_chunks (
  id SERIAL PRIMARY KEY,
  source_id TEXT NOT NULL,
  chunk_id TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  url TEXT,
  embedding VECTOR(1024), -- Compatible with local BERT/Gemma embeddings or adaptable
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(source_id, chunk_id)
);

CREATE INDEX IF NOT EXISTS idx_policy_chunks_content_trgm ON policy_chunks USING gin (to_tsvector('english', content));
`;

const SEED_DATA = [
  {
    source_id: "iv_guideline_2025",
    chunk_id: "iv_eligibility_basic",
    title: "IV Eligibility - Basic Conditions",
    content: "To be eligible for Invalidenversicherung (IV) benefits in Switzerland, you must meet three basic conditions: 1) You must be insured in Switzerland (residence or employment). 2) You must have a health impairment that restricts your ability to work or perform daily tasks. 3) The incapacity to work must be likely to last at least one year.",
    url: "https://www.ahv-iv.ch/en/Social-insurances/Invalidity-insurance-IV",
    metadata: { authority_tier: 1, canton: "Federal" }
  },
  {
    source_id: "iv_guideline_2025",
    chunk_id: "iv_registration_process",
    title: "How to Register for IV",
    content: "You should register for IV as soon as you notice that a health impairment could threaten your job or your ability to perform daily tasks for a longer period (at least 6 months). Early detection is key. You can register using the official form 'Anmeldung für Erwachsene: Berufliche Integration/Rente' available from your cantonal IV office.",
    url: "https://www.ahv-iv.ch/en/Leaflets-forms/Forms/Invalidity-insurance-IV",
    metadata: { authority_tier: 1, canton: "Federal" }
  },
  {
    source_id: "zh_social_services",
    chunk_id: "zh_supplementary_benefits",
    title: "Supplementary Benefits in Zurich",
    content: "If your IV pension and other income are not enough to cover your minimal living costs, you may be entitled to Supplementary Benefits (Ergänzungsleistungen/EL). In the Canton of Zurich, you must apply for EL at your municipal SVA office. The calculation considers your recognized expenses (rent, health insurance) versus your income.",
    url: "https://www.svazurich.ch/el",
    metadata: { authority_tier: 2, canton: "ZH" }
  }
];

async function run() {
  try {
    await client.connect();
    console.log('Connected to database.');

    console.log('Applying schema...');
    await client.query(SCHEMA_SQL);
    console.log('Schema applied.');

    console.log('Seeding data...');
    for (const row of SEED_DATA) {
      const query = `
        INSERT INTO policy_chunks (source_id, chunk_id, title, content, url, metadata)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (source_id, chunk_id) 
        DO UPDATE SET content = EXCLUDED.content, title = EXCLUDED.title, url = EXCLUDED.url;
      `;
      await client.query(query, [row.source_id, row.chunk_id, row.title, row.content, row.url, row.metadata]);
    }
    console.log(`Seeded ${SEED_DATA.length} policy chunks.`);

  } catch (err) {
    console.error('Error:', err);
    process.exit(1);
  } finally {
    await client.end();
  }
}

run();
