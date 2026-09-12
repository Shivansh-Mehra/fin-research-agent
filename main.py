import os
from dotenv import load_dotenv
from src.agent.graph import build_graph

load_dotenv()

def main():
    print("Initializing Multi-Agent Financial Researcher...\n")
    
    app = build_graph()
    
    # Test Query
    query = "What are the main operational risks for the company, and is there any recent news regarding their supply chain?"
    
    print(f"Submitting Query: {query}")
    
    # invoke() starts the graph execution from the START node
    result = app.invoke({"query": query, "iterations": 0})
    
    print("\n" + "="*60)
    print("FINAL INTELLIGENCE REPORT:")
    print("="*60)
    print(result["report"])

if __name__ == "__main__":
    main()