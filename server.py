
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

# Global placeholder
controller = None

def get_controller():
    global controller
    if controller:
        return controller
        
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("WARNING: OPENAI_API_KEY not found during initialization.")
        return None

    try:
        print("Initializing pipeline...")
        adapter = OpenAIAdapter()
        
        if api_key:
            print("Using OpenAI Embeddings")
            idx = OpenAIIndex()
        else:
            # This branch might not be reachable due to check above, but keeping logic
            print("Using Simple MD5 Embeddings")
            idx = SimpleVectorIndex()

        idx.add("doc1", "This product is excellent and works as expected.")
        idx.add("doc2", "The device is not working after a week.")
        idx.add("doc3", "Customer support was very helpful.")
        
        controller = PipelineController(adapter=adapter, vector_index=idx)
        return controller

    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        # Store the error to return it
        global init_error
        init_error = str(e)
        return None

# Global error storage
init_error = None

class AnalyzeRequest(BaseModel):
    text: str

@app.post("/api/analyze")
async def analyze_text(request: AnalyzeRequest):
    ctrl = get_controller()
    if not ctrl:
        if not os.environ.get("OPENAI_API_KEY"):
            raise HTTPException(status_code=500, detail="Pipeline not initialized: OPENAI_API_KEY is missing on the server.")
        
        # Return the actual error
        detail_msg = f"Pipeline initialization failed: {init_error}" if init_error else "Pipeline initialization failed. Check server logs."
        raise HTTPException(status_code=500, detail=detail_msg)
    
    try:
        result = ctrl.run(request.text)
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
