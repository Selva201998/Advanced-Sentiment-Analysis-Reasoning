
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pipeline.controller import PipelineController
from adapters.openai_adapter import OpenAIAdapter
from embeddings.simple_embedding import SimpleVectorIndex
from embeddings.openai_embedding import OpenAIIndex
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

app = FastAPI()

# Initialize pipeline components
# We do this globally so we don't reload for every request
if not os.environ.get("OPENAI_API_KEY"):
    print("WARNING: OPENAI_API_KEY not found. Web UI might fail.")

try:
    adapter = OpenAIAdapter()
    
    # Choose embedding index based on API key availability
    if os.environ.get("OPENAI_API_KEY"):
        print("Using OpenAI Embeddings")
        idx = OpenAIIndex()
    else:
        print("Using Simple MD5 Embeddings")
        idx = SimpleVectorIndex()

    idx.add("doc1", "This product is excellent and works as expected.")
    idx.add("doc2", "The device is not working after a week.")
    idx.add("doc3", "Customer support was very helpful.")
    
    controller = PipelineController(adapter=adapter, vector_index=idx)
except Exception as e:
    print(f"Error initializing pipeline: {e}")
    controller = None

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/api/analyze")
async def analyze_text(request: AnalyzeRequest):
    if not controller:
        raise HTTPException(status_code=500, detail="Pipeline not initialized (check API Key)")
    
    try:
        result = controller.run(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files (HTML, CSS, JS)
# Mount this LAST to avoid overriding API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/status")
async def get_status():
    key = os.environ.get("OPENAI_API_KEY")
    return {
        "status": "online",
        "pipeline_initialized": controller is not None,
        "api_key_configured": bool(key),
        "api_key_length": len(key) if key else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
