from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent.graph import build_graph
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = FastAPI(title="Multi-Agent Financial Researcher", version="1.0")

# Initialize the graph once when the server starts
agent_app = build_graph()

# Define the expected JSON payload
class ResearchRequest(BaseModel):
    query: str

@app.post("/research")
async def run_research(request: ResearchRequest):
    try:
        # Pass the query into our state machine
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