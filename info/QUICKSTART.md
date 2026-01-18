# 🚀 AI Insurance Underwriting System - Quickstart

## ✅ Build Status
- **Architecture**: 3-Phase Model (RAG -> LLM Chains -> Orchestration)
- **Framework**: LangChain + Google Gemini
- **RAG Engine**: FAISS + LCEL
- **SSL Support**: Patched for Corporate Proxies

## 🛠️ Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Config**
   - The system is pre-configured with the Google API Key found in your codebase.
   - ⚠️ **Note**: If you see `RetryError` or `404`, please update `GOOGLE_API_KEY` in `.env` with a fresh key from [Google AI Studio](https://aistudio.google.com/).

3. **Run the Demo**
   ```bash
   python terminal_demo.py
   ```

4. **Run Advanced Workflow**
   ```bash
   python src/pipeline/langgraph_workflow.py
   ```

## 📂 Key Files
- `src/core/rag_pipeline.py`: The brain of the RAG system.
- `src/core/ssl_handler.py`: The fix for SSL certificate errors.
- `terminal_demo.py`: The execution display.
