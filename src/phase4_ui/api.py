import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.phase3_rag.rag_logic import RAGEngine

app = FastAPI(title="Mutual Fund FAQ Assistant API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
try:
    engine = RAGEngine()
except Exception as e:
    print(f"Error initializing RAG Engine: {e}")
    engine = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "engine_ready": engine is not None}

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    if not engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized.")
    
    try:
        response_text = engine.process_query(request.query)
        return QueryResponse(answer=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi.middleware.cors import CORSMiddleware

# This is your "Guest List"
origins = [
    "https://groww-mf-saathi111-huvirxceh-asha-s-projects3.vercel.app", # Your Vercel URL
    "http://localhost:5173", # This lets you test on your own computer
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all types of actions (Ask, Delete, etc.)
    allow_headers=["*"], # Allows all types of data sent by your frontend
)