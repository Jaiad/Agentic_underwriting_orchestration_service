# Agentic Underwriting System (5 Pillars Edition)

This is a complete upgrade of the underwriting pipeline using **LangGraph**, **LangSmith**, and **Gemini 2.0 Flash**. It strictly adheres to the "5 Pillars of Agentic AI" and maintains output parity with the original Regex/RAG demos.

## 🏗️ Architecture

The system is built as a parallel `StateGraph` in `src/graph_pipeline/`.

### The 5 Pillars
1.  **Reliability 🏛️**: 
    *   Strict **Pydantic Validation** on extraction (Reliability).
    *   **Deterministic Math** for premium calculations (Output Parity).
2.  **Security 🛡️**: 
    *   **Guardrail Node** (`node_security_scan`) runs before any logic to block PII/Injection.
3.  **Cost 💰**: 
    *   **Token/Cost Tracking** implemented per-node.
    *   Optimized using **Gemini 2.0 Flash**.
4.  **Operation ⚙️**: 
    *   **LangSmith Tracing** enabled.
    *   **Checkpointing** with `MemorySaver` for Human-in-the-Loop workflows.
    *   **Thread ID** management for conversation persistence.
5.  **Performance 🚀**: 
    *   **Parallel Execution** of `Industry Classification`, `Rate Discovery`, and `Risk Assessment`.

## 📂 Key Files

*   **`web_app_agentic.py`**: The **NEW Professional Web UI**. Running on Port **8004**.
    *   Features a new "🧠 Agentic Intelligence" tab.
*   **`run_agentic_demo.py`**: The **CLI Entry Point**.
    *   Produces the colorful "Terminal Demo" output you are used to.
*   **`src/graph_pipeline/`**:
    *   `graph.py`: The Main Orchestrator.
    *   `nodes.py`: The Logic (Security, Extraction, Math).
    *   `state.py`: The State Schema with Reducers.

## 🏃 controls

### 1. Run the Web UI (Recommended)
```bash
python web_app_agentic.py
# Access at http://localhost:8004
```

### 2. Run the CLI Demo
```bash
python run_agentic_demo.py
```
