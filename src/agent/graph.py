from langgraph.graph import StateGraph, END, START
from src.agent.state import GraphState
from src.agent.nodes import planner_node, db_node, web_node, reviewer_node

def route_evaluation(state: GraphState):
    # Hard stop to prevent runaway token consumption loops
    if state["iterations"] > 2:
        return END
    if state["is_valid"]:
        return END
    return "planner"

def build_graph():
    workflow = StateGraph(GraphState)
    
    # Register the workers
    workflow.add_node("planner", planner_node)
    workflow.add_node("db_search", db_node)
    workflow.add_node("web_search", web_node)
    workflow.add_node("reviewer", reviewer_node)
    
    # Connect the execution flow
    workflow.add_edge(START, "planner")
    
    # Parallel fan-out execution
    workflow.add_edge("planner", "db_search")
    workflow.add_edge("planner", "web_search")
    
    # Converge back at the reviewer
    workflow.add_edge(["db_search", "web_search"], "reviewer")
    
    # Evaluate and route conditionally
    workflow.add_conditional_edges(
        "reviewer", 
        route_evaluation,
        {"planner": "planner", END: END}
    )
    
    return workflow.compile()