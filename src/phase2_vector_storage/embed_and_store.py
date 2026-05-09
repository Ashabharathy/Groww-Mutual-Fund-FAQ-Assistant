import os
import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

CORPUS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'phase1_data_acquisition', 'data', 'final', 'corpus_chunks.json')
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), 'chroma_db')

def embed_and_store():
    print(f"[Phase 2] Loading corpus chunks from {CORPUS_FILE}...")
    if not os.path.exists(CORPUS_FILE):
        print("Error: corpus_chunks.json not found. Did you run Phase 1?")
        return
        
    with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
        chunks_data = json.load(f)
        
    print(f"[Phase 2] Loaded {len(chunks_data)} chunks. Creating Document objects...")
    documents = []
    for chunk in chunks_data:
        doc = Document(
            page_content=chunk["text"],
            metadata={
                "chunk_id": chunk["chunk_id"],
                "source_url": chunk["metadata"]["source_url"],
                "amc_name": chunk["metadata"]["amc_name"],
                "scheme_name": chunk["metadata"]["scheme_name"],
                "last_updated_date": chunk["metadata"]["last_updated_date"]
            }
        )
        documents.append(doc)
        
    print("[Phase 2] Initializing BAAI/bge-small-en-v1.5 embedding model...")
    # Using HuggingFaceEmbeddings which uses sentence-transformers under the hood
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    print(f"[Phase 2] Creating and persisting Vector Database at {CHROMA_DB_DIR}...")
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    
    # Store in ChromaDB
    # Note: Chroma will automatically embed the documents here
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
        collection_name="tata_mutual_funds"
    )
    
    print("[Phase 2] Embedding and Storage Complete! Database is ready for Phase 3.")

if __name__ == "__main__":
    embed_and_store()
