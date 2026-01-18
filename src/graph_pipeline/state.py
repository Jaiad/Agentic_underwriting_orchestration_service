"""
State Definition for Agentic Underwriting Pipeline.
Uses advanced LangGraph concepts such as Annotated reducers to handle concurrent updates from parallel nodes.
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from operator import add
from pydantic import BaseModel, Field

def merge_dicts(a: Dict, b: Dict) -> Dict:
    """Reducer to merge two dictionaries."""
    return {**a, **b}

# --- Pydantic Models ---

class ExtractedData(BaseModel):
    client_name: str = Field(description="Name of the client/company")
    industry: str = Field(description="Industry type")
    revenue: float = Field(description="Annual revenue in USD")
    employees: int = Field(description="Number of employees")
    address: Optional[str] = Field(description="Business address")
    coverage_needs: List[str] = Field(description="List of requested coverages")

class CalculationResult(BaseModel):
    gl_base: float
    gl_formula: str
    loss_modifier: float
    loss_percent: str
    loss_formula: str
    auto_premium: float
    auto_formula: str
    auto_formula_desc: str
    final_premium: float
    authority: str
    coverage_analysis: str

# --- Main Agent State ---

class AgentState(TypedDict):
    """
    The central state of the LangGraph application.
    """
    # 1. Input/Output
    input_email: str
    quote_id: str
    
    # 2. Pipeline Data - Nodes write to distinct keys
    extracted_data: Optional[Dict[str, Any]]
    industry_classification: Optional[Dict[str, Any]]
    rates: Optional[List[Dict[str, Any]]]
    risk_assessment: Optional[Dict[str, Any]]
    calculation: Optional[Dict[str, Any]]
    quote_letter: Optional[str]
    
    # 3. Control Flow
    error: Optional[str]
    is_referral: bool
    is_approved: Optional[bool]
    
    # 4. 5 Pillars Metrics - Using separate keys with reducers for concurrency
    # These use Annotated[..., merge_dicts] so parallel nodes can all write to them safely.
    cost_tracking: Annotated[Dict[str, float], merge_dicts]
    execution_time: Annotated[Dict[str, float], merge_dicts]
    security_flags: Annotated[List[str], add]
    pillars: Optional[Dict] # For backward compat in UI (aggregated later)
