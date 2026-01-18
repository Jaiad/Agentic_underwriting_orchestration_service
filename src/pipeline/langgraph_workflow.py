"""
LangGraph Workflow for Insurance Underwriting.
Implements the 3-Phase Model as a state machine using LangGraph.
"""

from typing import TypedDict, Dict, Any, List
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    # Fallback/Placeholder if langgraph is not installed (it's new)
    StateGraph = None
    END = "END"
    print("Warning: langgraph not installed. Graph features will be simulated.")

from langchain_core.messages import BaseMessage, HumanMessage
from src.core.rag_pipeline import get_rag_pipeline

# Define State
class AgentState(TypedDict):
    INPUT: str
    email_data: Dict[str, Any]
    industry: str
    rates: List[Dict]
    premium: float
    risk_score: int
    final_output: str

# Define Nodes
def parse_email(state: AgentState):
    print("  ⚪ [Graph] Parsing Email...")
    # Simulation of parsing logic using LLM
    # In real impl, we'd call the EmailParserStep chain here
    return {"email_data": {"client": "ABC Corp", "revenue": 15000000}}

def classify_industry(state: AgentState):
    print("  ⚪ [Graph] Classifying Industry (RAG)...")
    rag = get_rag_pipeline()
    # Use RAG to get context
    context = rag.query("Construction industry codes")
    return {"industry": "Construction (BIC 0044)"}

def calculate_premium(state: AgentState):
    print("  ⚪ [Graph] Calculating Premium...")
    return {"premium": 165375.00}

def assess_risk(state: AgentState):
    print("  ⚪ [Graph] Assessing Risk...")
    return {"risk_score": 65}

# Build Graph
def build_underwriting_graph():
    if not StateGraph:
        return None
        
    workflow = StateGraph(AgentState)
    
    workflow.add_node("parser", parse_email)
    workflow.add_node("classifier", classify_industry)
    workflow.add_node("calculator", calculate_premium)
    workflow.add_node("risk_assessor", assess_risk)
    
    workflow.set_entry_point("parser")
    
    workflow.add_edge("parser", "classifier")
    workflow.add_edge("classifier", "calculator")
    workflow.add_edge("calculator", "risk_assessor")
    workflow.add_edge("risk_assessor", END)
    
    app = workflow.compile()
    return app

def run_graph_demo(email_content: str):
    print("\n🚀 Executing LangGraph Workflow...")
    app = build_underwriting_graph()
    if app:
        initial_state = {"INPUT": email_content}
        for chunk in app.stream(initial_state):
            # Print state updates
            for key, value in chunk.items():
                pass # Already printing in nodes
        print("✅ Graph Execution Complete")
    else:
        print("LangGraph not available - skipping graph demo.")
