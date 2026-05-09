import os
import sys

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_store import VectorStore

def test_queries():
    db_path = os.path.join("src", "phase2_embedding_storage", "data", "vector_db")
    vs = VectorStore(db_path=db_path)
    
    queries = [
        "What is the expense ratio of Tata Small Cap Fund?",
        "What is the exit load for Tata Digital India Fund?",
        "Minimum SIP amount for Tata Ethical Fund"
    ]
    
    print("\n--- Testing Retrieval ---")
    for q in queries:
        print(f"\nQuery: {q}")
        results = vs.query(q, n_results=2)
        
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            dist = results['distances'][0][i]
            print(f"Result {i+1} (Dist: {dist:.4f}):")
            print(f"Scheme: {meta['scheme_name']}")
            print(f"Snippet: {doc[:200]}...")
            print(f"Source: {meta['source_url']}")

if __name__ == "__main__":
    test_queries()
