import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Start the app
app = FastAPI(title="Mutual Fund FAQ Assistant API")

# 2. The Guest List (CORS) - MUST BE AT THE TOP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows local frontend and any origin in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Path setup for your RAG engine
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.phase3_rag.rag_logic import RAGEngine

# 4. Initialize Engine
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

# 5. Start command for Railway
if _name_ == "_main_":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)