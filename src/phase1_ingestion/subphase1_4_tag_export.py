import os
import json
from datetime import datetime

CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'phase1_cleaned')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'corpus_chunks.json')

def tag_and_export():
    print("[Subphase 1.4] Starting Metadata Tagging & Export...")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    all_chunks = []
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    if not os.path.exists(CLEAN_DIR):
        print(f"[Subphase 1.4] Cleaned directory not found: {CLEAN_DIR}")
        return

    for filename in os.listdir(CLEAN_DIR):
        if not filename.endswith('_chunks.json'):
            continue
            
        file_path = os.path.join(CLEAN_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        scheme_name = data["scheme_name"]
        source_url = data["source_url"]
        
        for i, chunk_text in enumerate(data["chunks"]):
            all_chunks.append({
                "chunk_id": f"{scheme_name.replace(' ', '_')}_{i}",
                "text": chunk_text,
                "metadata": {
                    "source_url": source_url,
                    "amc_name": "Tata Mutual Fund",
                    "scheme_name": scheme_name,
                    "last_updated_date": today_date
                }
            })
            
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=4, ensure_ascii=False)
        
    print(f"[Subphase 1.4] Tagging Complete. Successfully saved {len(all_chunks)} chunks to {OUTPUT_FILE}\n")

if __name__ == "__main__":
    tag_and_export()
