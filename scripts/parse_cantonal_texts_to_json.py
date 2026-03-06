#!/usr/bin/env python3
"""
parse_cantonal_texts_to_json.py

Reads `data/sources/cantonal/sources.config.json` to find all scraped cantonal sub-pages.
For each sub-page, it reads the corresponding `.txt` file content and combines it
with the metadata (language, topics, URL, source ID) into a JSON array.

This output JSON can then be fed directly into `scripts/chunk-and-load-policy.js`
to populate the Postgres `policy_chunks` table for the RAG pipeline.
"""

import json
import os
import sys

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, "data", "sources", "cantonal", "sources.config.json")
    output_path = os.path.join(base_dir, "data", "documents", "cantonal", "parsed_cantonal_policies.json")

    if not os.path.exists(config_path):
        print(f"Error: Could not find config at {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    documents = []

    for source in config.get("sources", []):
        canton = source.get("canton", "Unknown")
        jurisdiction = "Canton"
        
        for page in source.get("scraped_pages", []):
            local_file = page.get("local_file")
            
            if not local_file:
                print(f"Warning: No local_file defined for {page.get('source_id')}")
                continue
                
            file_path = os.path.join(base_dir, "data", local_file)
            
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue
                
            with open(file_path, "r", encoding="utf-8") as text_file:
                content = text_file.read()
                
            # Create the document structure required by chunk-and-load-policy.js
            doc = {
                "source_id": page.get("source_id"),
                "title": page.get("title"),
                "url": page.get("url"),
                "content": content,
                "metadata": {
                    "authority_tier": 2, # Cantonal policy
                    "jurisdiction": jurisdiction,
                    "canton": canton,
                    "language": page.get("language", "de"),
                    "topics": page.get("topics", []),
                    "fetched_at": page.get("fetched_at")
                }
            }
            documents.append(doc)
            print(f"Parsed {page.get('source_id')} from {local_file}")

    # Write the combined JSON
    out_dir = os.path.dirname(output_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
        
    print(f"\nSuccessfully parsed {len(documents)} cantonal policy documents.")
    print(f"Output written to: {output_path}")
    print("\nYou can now run the RAG chunker with:")
    print(f"node scripts/chunk-and-load-policy.js data/documents/cantonal/parsed_cantonal_policies.json")

if __name__ == "__main__":
    main()
