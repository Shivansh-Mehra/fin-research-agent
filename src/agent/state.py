from typing import TypedDict

class GraphState(TypedDict):
    query: str
    search_queries: list[str]  # Holds the Planner's decomposed queries [db_query, web_query]
    db_context: list[str]      # SEC Filing chunks
    web_context: list[str]     # Live Tavily news
    report: str
    is_valid: bool
    iterations: int            # Prevents infinite retry loops