import os
import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from src.agent.state import GraphState
from src.db.vector_store import get_vector_store
from src.tools.web_search import get_web_search_tool

def get_llm():
    return ChatGroq(
        temperature=0, 
        model_name=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    )

def planner_node(state: GraphState):
    print("\n[PLANNER] Decomposing query...")
    query = state["query"]
    llm = get_llm()
    
    prompt = f"""You are a financial research planner. 
Break this query into 2 distinct, highly targeted search queries:
1. A semantic search query for extracting risk factors/metrics from internal SEC PDF databases.
2. A web search query for finding real-time news related to the topic.
Query: {query}
Return ONLY a JSON object with keys 'db_query' and 'web_query'. No markdown formatting."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        content = response.content.replace("```json", "").replace("```", "").strip()
        queries = json.loads(content)
        search_queries = [queries.get("db_query", query), queries.get("web_query", query)]
    except:
        # Fallback if the LLM fails to format JSON correctly
        search_queries = [query, query]
        
    return {"search_queries": search_queries, "iterations": state.get("iterations", 0) + 1}
    
def db_node(state: GraphState):
    print("[DATABASE] Extracting grounded intelligence from pgvector...")
    db_query = state["search_queries"][0]
    store = get_vector_store()
    
    results = store.similarity_search(db_query, k=3)
    context = [doc.page_content for doc in results]
    return {"db_context": context}

def web_node(state: GraphState):
    print("[WEB] Sweeping real-time market news via Tavily...")
    web_query = state["search_queries"][1]
    tool = get_web_search_tool()
    
    try:
        results = tool.invoke({"query": web_query})
        context = [doc["content"] for doc in results]
    except Exception as e:
        context = [f"Web search failed: {e}"]
        
    return {"web_context": context}

def reviewer_node(state: GraphState):
    print("[REVIEWER] Synthesizing data and evaluating completeness...")
    llm = get_llm()
    query = state["query"]
    db_ctx = "\n".join(state.get("db_context", []))
    web_ctx = "\n".join(state.get("web_context", []))
    
    prompt = f"""You are a senior financial analyst.
Synthesize the provided SEC data and Live News into a professional final report answering: {query}
If the provided data is completely insufficient to answer the core prompt, output exactly and only: "INSUFFICIENT_DATA"

SEC Data:
{db_ctx}

Live News:
{web_ctx}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    
    if "INSUFFICIENT_DATA" in content:
        print("[REVIEWER] Missing critical context. Triggering retry loop.")
        return {"is_valid": False, "report": "Missing critical context. Retrying..."}
        
    return {"is_valid": True, "report": content}