"""
scheduler.py — Local pipeline scheduler for the Groww MF Saathi RAG system.

Runs the full data refresh pipeline on a schedule:
  Phase 1.2 → Scrape latest HTML from Groww (Playwright)
  Phase 1.3 → Clean & chunk the HTML into semantic chunks
  Phase 1.4 → Tag & export to corpus_chunks.json
  Phase 2   → Re-embed all chunks and rebuild the FAISS index

Usage:
  python scheduler.py              # Run once immediately, then on schedule
  python scheduler.py --run-once   # Run the pipeline once and exit
"""

import os
import sys
import asyncio
import logging
import argparse
import schedule
import time
from datetime import datetime

# ── Logging setup ────────────────────────────────────────────────────────────
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOG_DIR, "scheduler.log"), encoding="utf-8"),
    ],
)
log = logging.getLogger("scheduler")

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
PHASE1_DIR = os.path.join(ROOT, "src", "phase1_ingestion")
PHASE2_DIR = os.path.join(ROOT, "src", "phase2_embedding")

sys.path.insert(0, PHASE1_DIR)
sys.path.insert(0, PHASE2_DIR)

# ── Pipeline steps ────────────────────────────────────────────────────────────

def step_extract():
    """Phase 1.2 — Scrape all 15 Groww fund pages with Playwright."""
    log.info("━━━ Step 1/4 · Scraping fund pages (Playwright) ━━━")
    import subphase1_2_extract
    asyncio.run(subphase1_2_extract.extract_all())
    log.info("✔  Scraping complete.")


def step_chunk():
    """Phase 1.3 — Clean HTML and produce semantic chunks."""
    log.info("━━━ Step 2/4 · Cleaning & chunking HTML ━━━")
    import subphase1_3_clean_chunk
    subphase1_3_clean_chunk.clean_and_chunk_all()
    log.info("✔  Chunking complete.")


def step_export():
    """Phase 1.4 — Tag chunks with metadata and export corpus_chunks.json."""
    log.info("━━━ Step 3/4 · Tagging & exporting corpus ━━━")
    import subphase1_4_tag_export
    subphase1_4_tag_export.tag_and_export()
    log.info("✔  Export complete.")


def step_embed():
    """Phase 2 — Re-embed all chunks and rebuild the FAISS index from scratch."""
    log.info("━━━ Step 4/4 · Re-embedding & rebuilding FAISS index ━━━")

    # Use offline mode only when the HF cache already exists (local runs).
    # On GitHub Actions the cache is restored before this step, so the model
    # will be present; on a cold runner it will download normally.
    hf_cache = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    model_cached = os.path.isdir(os.path.join(hf_cache, "models--sentence-transformers--all-MiniLM-L6-v2"))
    if model_cached:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        log.info("  HF model found in cache — using offline mode.")
    else:
        log.info("  HF model not cached — will download from HuggingFace.")

    # Delete old index so we get a clean rebuild (not an append)
    db_path = os.path.join(ROOT, "data", "phase2_vector_db")
    for fname in ("faiss_index.bin", "metadata.pkl"):
        fpath = os.path.join(db_path, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            log.info(f"  Removed old {fname}")

    # Change cwd to project root so relative paths in run_phase2.py resolve
    original_cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        from vector_store import VectorStore
        chunks_path = os.path.join("data", "corpus_chunks.json")
        vs = VectorStore(db_path=db_path)
        chunks = vs.load_chunks(chunks_path)
        log.info(f"  Loaded {len(chunks)} chunks for embedding.")
        vs.add_chunks_to_db(chunks)
        log.info(f"✔  FAISS index rebuilt with {len(chunks)} vectors.")
    finally:
        os.chdir(original_cwd)


# ── Full pipeline ─────────────────────────────────────────────────────────────

def run_pipeline():
    start = datetime.now()
    log.info("=" * 60)
    log.info(f"  PIPELINE START  —  {start.strftime('%Y-%m-%d %H:%M:%S')}")
    log.info("=" * 60)

    try:
        step_extract()
        step_chunk()
        step_export()
        step_embed()

        elapsed = (datetime.now() - start).seconds
        log.info("=" * 60)
        log.info(f"  PIPELINE COMPLETE  —  {elapsed}s elapsed")
        log.info("=" * 60)

    except Exception as e:
        log.error(f"  PIPELINE FAILED: {e}", exc_info=True)
        log.info("=" * 60)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Groww MF Saathi — Data Refresh Scheduler")
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run the pipeline once immediately and exit (no scheduling).",
    )
    parser.add_argument(
        "--time",
        default="02:00",
        metavar="HH:MM",
        help="Daily run time in 24h format (default: 02:00).",
    )
    args = parser.parse_args()

    if args.run_once:
        log.info("Mode: run-once")
        run_pipeline()
        sys.exit(0)

    # Scheduled mode — run immediately once, then daily at --time
    log.info(f"Mode: scheduled  (daily at {args.time})")
    log.info("Running pipeline immediately on startup...")
    run_pipeline()

    schedule.every().day.at(args.time).do(run_pipeline)
    log.info(f"Next scheduled run: {args.time} daily.  Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        log.info("Scheduler stopped by user.")
