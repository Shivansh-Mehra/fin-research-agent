from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from src.agent.graph import build_graph
from dotenv import load_dotenv, find_dotenv
import os
import shutil

# Import your actual ingestion function!
from ingest import ingest_documents 

load_dotenv(find_dotenv())

app = FastAPI(title="Multi-Agent Financial Researcher", version="1.0")
agent_app = build_graph()

class ResearchRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_and_ingest(file: UploadFile = File(...)):
    try:
        # 1. Ensure the data directory exists
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{file.filename}"
        
        # 2. Save the uploaded file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 3. Trigger your exact ingestion script
        ingest_documents("data")
        
        return {"status": "success", "message": f"Successfully ingested {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research")
async def run_research(request: ResearchRequest):
    # ... your existing research endpoint code ...
    try:
        result = agent_app.invoke({"query": request.query, "iterations": 0})
        return {
            "status": "success",
            "report": result["report"],
            "sources_checked": {
                "db_chunks": len(result.get("db_context", [])),
                "web_articles": len(result.get("web_context", []))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}