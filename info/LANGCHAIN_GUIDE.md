# 🦜🔗 LangChain Concepts Integration Guide

Per your request to use more LangChain concepts, we have analyzed your API keys, identified a working model (**gemini-2.0-flash-exp**), and implemented two advanced demonstration files.

## 1. Advanced Orchestration (LCEL & Structured Data)
**File:** `langchain_orchestrator_advanced.py`

This file demonstrates how to move away from Regex/Parsing to intelligent extraction using **Pydantic** and **LCEL**.

### Key Concepts:
- **LCEL (LangChain Expression Language)**:
  ```python
  chain = prompt | model | parser
  ```
  This creates readable, composable workflows.
- **Structured Output**: Uses `PydanticOutputParser` to force the LLM to return valid JSON fitting your `InsuranceExtraction` schema.
- **Prompt Templates**: Separates the instructions from the data.

**Run it:**
```bash
python langchain_orchestrator_advanced.py
```

## 2. RAG (Retrieval Augmented Generation)
**File:** `langchain_rag_tutorial.py`

This file enables your model to "read" external guidelines before answering, fixing the "hallucination" problem.

### Key Concepts:
- **Embeddings**: Uses `GoogleGenerativeAIEmbeddings` to understand text semantics.
- **Vector Store (FAISS)**: Stores the knowledge base efficiently.
- **Retrieval Chain**: Dynamically fetches the right context for every question.

**Run it:**
```bash
python langchain_rag_tutorial.py
```

## 3. API & Model Diagnostic
**File:** `test_api_models.py`

We used this to confirm that your current environment works best with `gemini-2.0-flash-exp`.

## Recommended Next Steps
To fully modernize your main `web_app.py`:
1.  **Replace** the regex logic in `langchain_orchestrator.py` with the `AdvancedOrchestrator` class from the new file.
2.  **Integrate** the RAG pipeline by loading your PDF/Docs into the `data/` folder and connecting the `RAGPipeline` (which we verified in `src/core/rag_pipeline.py`).
