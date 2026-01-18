# LangChain Concepts Guide

Start with `langchain_orchestrator_advanced.py`. This file Upgrades the logic from Regex/Mock to a production-grade LangChain pipeline.

## Concepts Implemented

### 1. LangChain Expression Language (LCEL)
We replaced manual function calls with the declarative Pipe syntax (`|`).
```python
chain = prompt | model | parser
```
This makes chains easy to read ("Take prompt, pass to model, pass to parser").

### 2. Structured Output with Pydantic
Instead of asking for "JSON" and using `json.loads` (which is fragile), we use `PydanticOutputParser`.
- We defined `class InsuranceExtraction(BaseModel)`.
- The parser automatically inserts `format_instructions` into the prompt.
- The output is validated against the schema.

### 3. Prompt Templates
We moved hardcoded strings into `ChatPromptTemplate`.
```python
("system", "You are an expert..."),
("human", "{email}")
```

### 4. Chat Models (Google Gemini)
We integrated `ChatGoogleGenerativeAI` to use the latest Gemini models.
*Note: We found that **`gemini-2.0-flash-exp`** is the reliable model for your current API key.*

## How to Run
```bash
python langchain_orchestrator_advanced.py
```
*Likely requires fixing SSL/Proxy/Key issues if you see connection errors.*
