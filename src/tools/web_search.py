import os
from langchain_community.tools.tavily_search import TavilySearchResults

def get_web_search_tool():
    # Tavily automatically detects the TAVILY_API_KEY from your .env
    return TavilySearchResults(max_results=3)