
"""
RAG Web App Server
------------------
Serves the RAG implementation and the Professional React UI.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import sys

# Add root to path so we can import src
sys.path.append(os.getcwd())

from src.rag_source.rag_engine import RagUnderwritingEngine

app = FastAPI(title="AI Underwriting RAG Engine")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyAMNfmzMDjUl4XncYBF2yEu_xvtJ-zkLzo")
rag_engine = RagUnderwritingEngine(api_key, data_dir="data/guidelines")

class QuoteRequest(BaseModel):
    email_content: str

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the single-file React UI"""
    with open("src/rag_source/rag_ui_react.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/process-rag-quote")
async def process_quote(request: QuoteRequest):
    """Process quote using the Real RAG Engine"""
    try:
        result = rag_engine.process_quote(request.email_content)
        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

if __name__ == "__main__":
    print("🚀 Starting RAG Web Server...")
    print("👉 ACCESS HERE: http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
