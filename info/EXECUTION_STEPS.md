# AI Insurance Underwriting Orchestrator - Execution Steps

## 🚀 Quick Start Guide

### Step 1: Run the Web Application
```powershell
venv\Scripts\python web_app.py
```

### Step 2: Access the Application
Open your browser and navigate to:
- **http://localhost:8000**
- **http://127.0.0.1:8000**

### Step 3: Use the Application
1. The sample email is pre-loaded
2. Click "🚀 Process Quote" button
3. Watch the AI process the request through 10 steps
4. View the generated quote with premium calculations

### Step 4: Present to Your Team
- Share the URL: **http://localhost:8000**
- Anyone on your network can access it
- Professional UI ready for demonstration

---

## 📋 Features

✅ **LangChain Integration** - Uses LangChain with Google Gemini  
✅ **10-Step AI Pipeline** - Complete underwriting workflow  
✅ **Professional UI** - Modern, responsive web interface  
✅ **Real-time Processing** - Live quote generation  
✅ **Risk Assessment** - Automated risk scoring  
✅ **Premium Calculation** - Dynamic pricing with modifiers  

---

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python)
- **AI Framework**: LangChain
- **LLM**: Google Gemini (gemini-1.5-flash)
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **API Key**: Already configured

---

## 🔧 Troubleshooting

If the server doesn't start:
```powershell
# Install dependencies
venv\Scripts\pip install fastapi uvicorn langchain langchain-google-genai

# Run again
venv\Scripts\python web_app.py
```

---

## 📊 API Endpoints

- `GET /` - Web UI
- `POST /api/process-quote` - Process quote request
- `GET /health` - Health check

---

## 🎯 For Presentation

1. **Start the server** - Run `web_app.py`
2. **Open browser** - Navigate to http://localhost:8000
3. **Demo the flow** - Click "Process Quote" with sample data
4. **Show results** - Highlight the premium, risk assessment, and quote letter
5. **Explain tech** - LangChain + Google Gemini integration

---

**Ready to present! 🎉**
