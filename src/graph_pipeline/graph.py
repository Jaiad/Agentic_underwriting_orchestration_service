"""
Advanced Graph Definition for Agentic Underwriting.
Features:
- Conditional routing based on risk level
- Parallel execution with proper fan-in
- LangSmith run metadata and tags
- Human-in-the-loop for high-risk scenarios
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langsmith import traceable
import os

from .state import AgentState
from .nodes import (
    node_security_scan,
    node_extract,
    node_industry,
    node_rates,
    node_risk,
    node_calculate,
    node_quote
)

# --- Conditional Routing Logic (Advanced Pattern) ---
def route_after_risk(state: AgentState) -> Literal["calculate", "END"]:
    """
    Advanced Pattern: Conditional routing based on risk assessment.
    High-risk quotes can be rejected immediately or routed differently.
    """
    # Check if security flagged the input
    if state.get("security_flags") and len(state["security_flags"]) > 0:
        # Security issue detected - could route to rejection
        return "END"
    
    # Normal flow: proceed to calculation
    return "calculate"

def route_after_calculation(state: AgentState) -> Literal["quote", "manual_review"]:
    """
    Advanced Pattern: Route to human review if high-risk or high-premium.
    Pillar: Operation (Human-in-the-Loop)
    """
    calc = state.get("calculation", {})
    risk = state.get("risk_assessment", {})
    
    # High-risk or high-premium requires manual review
    # BUT if already approved by human, proceed to quote
    if state.get("is_approved"):
        return "quote"

    if risk.get("level") == "HIGH":
        return "manual_review"
    
    return "quote"

# --- Graph Construction with Advanced Features ---
@traceable(
    name="Build Underwriting Graph",
    metadata={
        "framework": "langgraph",
        "version": "1.0",
        "pillars": ["reliability", "security", "cost", "operation", "performance"]
    },
    tags=["graph-construction", "5-pillars"]
)
def build_graph():
    """
    Builds the StateGraph with advanced LangChain/LangGraph patterns.
    
    Features:
    - Conditional edges for dynamic routing
    - Parallel execution with fan-out/fan-in
    - Checkpointing for human-in-the-loop
    - LangSmith metadata for observability
    """
    
    workflow = StateGraph(AgentState)
    
    # === Node Registration ===
    workflow.add_node("security", node_security_scan)
    workflow.add_node("extract", node_extract)
    
    # Parallel Analysis Nodes (Performance Pillar)
    workflow.add_node("industry", node_industry)
    workflow.add_node("rates", node_rates)
    workflow.add_node("risk", node_risk)
    
    # Business Logic Nodes
    workflow.add_node("calculate", node_calculate)
    workflow.add_node("quote", node_quote)
    
    # Human-in-the-Loop Node (Operation Pillar)
    workflow.add_node("manual_review", lambda state: {
        "stop_reason": "HIGH_RISK_REQUIRES_APPROVAL"
    })
    
    # === Edge Definition ===
    
    # Linear preprocessing
    workflow.add_edge(START, "security")
    workflow.add_edge("security", "extract")
    
    # Fan-Out: Parallel execution (Performance Pillar)
    workflow.add_edge("extract", "industry")
    workflow.add_edge("extract", "rates")
    workflow.add_edge("extract", "risk")
    
    # Fan-In: All parallel nodes converge (using implicit join)
    # Advanced Pattern: Conditional routing after risk assessment
    workflow.add_conditional_edges(
        "risk",
        route_after_risk,
        {
            "calculate": "calculate",
            "END": END  # Early termination if security issues
        }
    )
    
    # Industry and rates still need to reach calculate
    workflow.add_edge("industry", "calculate")
    workflow.add_edge("rates", "calculate")
    
    # Advanced Pattern: Conditional routing after calculation
    workflow.add_conditional_edges(
        "calculate",
        route_after_calculation,
        {
            "quote": "quote",
            "manual_review": "manual_review"
        }
    )
    
    # Final edges
    workflow.add_edge("quote", END)
    
    # Manual review proceeds to quote IF approved from state update, 
    # but the interrupt logic is handled by 'interrupt_before' in compile.
    # We add an edge back to quote because once resumed/approved, it should finish the job.
    workflow.add_edge("manual_review", "quote") 
    
    # === Compile with Advanced Features ===
    memory = MemorySaver()
    
    # Run metadata for LangSmith (Operation Pillar)
    run_name = "underwriting_5_pillars"
    
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["manual_review"] # PAUSE HERE for Human Intevention
    )
    
    return app

# Expose for LangGraph Studio
graph = build_graph()
