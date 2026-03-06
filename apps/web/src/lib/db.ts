/**
 * Shared PostgreSQL client for data export/delete (P1-11).
 * Uses DATABASE_URL or AUDIT_DATABASE_URL. Not used for audit write (audit-db has its own connection).
 */

import { Client } from "pg";

const DB_URL = process.env.DATABASE_URL || process.env.AUDIT_DATABASE_URL || "";

export function getDatabaseUrl(): string {
  return DB_URL.trim();
}

export function hasDatabase(): boolean {
  return getDatabaseUrl().length > 0;
}

/** Run a function with a dedicated client; client is always ended. */
export async function withDb<T>(fn: (client: Client) => Promise<T>): Promise<T> {
  const url = getDatabaseUrl();
  if (!url) throw new Error("DATABASE_URL (or AUDIT_DATABASE_URL) not set");
  const client = new Client({ connectionString: url });
  try {
    await client.connect();
    return await fn(client);
  } finally {
    await client.end();
  }
}
