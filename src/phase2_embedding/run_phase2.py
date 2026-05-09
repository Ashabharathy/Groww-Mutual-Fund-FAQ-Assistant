import os
import sys

# Add the current directory to sys.path to allow importing vector_store
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_store import VectorStore

def main():
    # Paths
    chunks_path = os.path.join("data", "corpus_chunks.json")
    db_path = os.path.join("data", "phase2_vector_db")
    
    print("--- Phase 2: Embedding & Vector Storage ---")
    
    # Initialize Vector Store
    vs = VectorStore(db_path=db_path)
    
    # Load Chunks
    try:
        chunks = vs.load_chunks(chunks_path)
        print(f"Loaded {len(chunks)} chunks from {chunks_path}")
    except Exception as e:
        print(f"Error loading chunks: {e}")
        return

    # Add Chunks to DB
    try:
        vs.add_chunks_to_db(chunks)
        print("Phase 2 completed successfully.")
    except Exception as e:
        print(f"Error during vector storage: {e}")
        return

if __name__ == "__main__":
    main()
