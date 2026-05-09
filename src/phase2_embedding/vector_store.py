import json
import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class VectorStore:
    def __init__(self, db_path="data/phase2_vector_db"):
        self.db_path = db_path
        self.index_path = os.path.join(self.db_path, "faiss_index.bin")
        self.metadata_path = os.path.join(self.db_path, "metadata.pkl")
        
        os.makedirs(self.db_path, exist_ok=True)
        
        # Load embedding model
        print("Loading embedding model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        self.index = None
        self.chunks_data = [] # List of {'chunk_id', 'text', 'metadata'}
        
        # Try to load existing index
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.load_index()

    def load_chunks(self, json_path):
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Chunks file not found at {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def add_chunks_to_db(self, chunks):
        print(f"Preparing {len(chunks)} chunks for embedding...")
        
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Initialize index if not exists
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.dimension)
            
        self.index.add(embeddings)
        self.chunks_data.extend(chunks)
        
        self.save_index()
        print("Successfully added all chunks and saved the index.")

    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.chunks_data, f)
        print(f"Index and metadata saved to {self.db_path}")

    def load_index(self):
        print(f"Loading existing index from {self.db_path}...")
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, 'rb') as f:
            self.chunks_data = pickle.load(f)
        print(f"Loaded {len(self.chunks_data)} chunks.")

    def query(self, query_text, n_results=3):
        if self.index is None:
            raise ValueError("Index is empty. Add chunks before querying.")
            
        # Embed and normalize query
        query_embedding = self.model.encode([query_text], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, n_results)
        
        results = {
            'documents': [[]],
            'metadatas': [[]],
            'distances': [[]],
            'ids': [[]]
        }
        
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx == -1: continue
            
            chunk = self.chunks_data[idx]
            results['documents'][0].append(chunk['text'])
            results['metadatas'][0].append(chunk['metadata'])
            results['distances'][0].append(float(distances[0][i]))
            results['ids'][0].append(chunk['chunk_id'])
            
        return results

if __name__ == "__main__":
    # Test initialization
    vs = VectorStore()
    print("Vector Store initialized.")
