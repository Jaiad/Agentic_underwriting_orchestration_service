
"""
Professional Web UI for RAG-Based Underwriting System
FastAPI + Professional HTML/CSS/JS Interface (Matches Demo UI)
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import sys
import traceback

# Import SSL handler and apply it
from src.core.ssl_handler import configure_ssl_handling
configure_ssl_handling()

# Add root to path so we can import src
sys.path.append(os.getcwd())

# Import the RAG Engine
from src.rag_source.rag_engine import RagUnderwritingEngine

# Initialize FastAPI
app = FastAPI(title="AI Underwriting RAG Engine")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine with API Key
api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyAMNfmzMDjUl4XncYBF2yEu_xvtJ-zkLzo")
rag_engine = RagUnderwritingEngine(api_key, data_dir="data/guidelines")

print("="*70)
print("✅ Web UI initialized with RAG Engine")
print("⚡ Powered by Gemini 2.0 Flash + FAISS Vector Search")
print("="*70)

class QuoteRequest(BaseModel):
    email_content: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main UI"""
    return HTML_TEMPLATE

@app.post("/api/process-rag-quote")
async def process_quote(request: QuoteRequest):
    """Process quote using RAG Engine"""
    try:
        print(f"\n{'='*70}")
        print("📧 Processing RAG quote request")
        print(f"{'='*70}\n")
        
        # Call RAG Engine
        if not rag_engine:
            raise Exception("RAG Engine not initialized (API Key missing?)")
            
        result = rag_engine.process_quote(request.email_content)
        
        print(f"\n{'='*70}")
        print("✅ Quote generated successfully")
        print(f"{'='*70}\n")
        
        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print(f"{'='*70}\n")
        
        # Always return JSON even on error
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=200) # Return 200 so fetch doesn't throw, we handle valid JSON error

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "model": "RAG + Gemini 2.0 Flash"}

# Professional HTML Template (Matches Screenshot UI)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Insurance Underwriting | RAG Engine</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'Segoe UI', 'Roboto', Arial, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            padding: 20px;
            color: #1a1a1a;
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            background: white;
            padding: 25px 40px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .header-content h1 {
            color: #2c3e50;
            font-size: 1.8rem;
            margin-bottom: 5px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .header-content p {
            color: #64748b;
            font-size: 0.95rem;
        }

        .main-content {
            display: grid;
            grid-template-columns: 40% 60%;
            gap: 30px;
            min-height: 700px; /* Ensure height */
        }

        .panel {
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            height: 100%;
        }

        .panel-header {
            padding: 20px 25px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #fff;
        }

        .panel-header h2 {
            font-size: 1.1rem;
            font-weight: 600;
            color: #334155;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .panel-body {
            padding: 25px;
            flex-grow: 1;
            overflow-y: auto;
            min-height: 500px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: #64748b;
            font-weight: 500;
        }

        select {
            width: 100%;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            color: #334155;
            background-color: #f8fafc;
            outline: none;
            transition: all 0.2s;
            cursor: pointer;
        }

        textarea {
            width: 100%;
            height: 350px;
            padding: 15px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            font-family: 'Monaco', 'Menlo', monospace;
            resize: none;
            outline: none;
            background-color: #f8fafc;
            line-height: 1.5;
            transition: all 0.2s;
        }
        
        textarea:focus {
            border-color: #2563eb;
            background: white;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .button {
            background: #2563eb; 
            color: white;
            border: none;
            padding: 16px;
            font-size: 1rem;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            font-weight: 600;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }

        .button:hover {
            background-color: #1d4ed8;
            transform: translateY(-1px);
        }

        /* Tabs System */
        .tabs {
            display: flex !important; /* Force Flex */
            flex-direction: row !important;
            gap: 5px;
            background: #f1f5f9;
            padding: 5px;
            border-radius: 10px;
            margin-bottom: 20px;
            width: 100%;
        }

        .tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #64748b;
            transition: all 0.2s;
        }

        .tab.active {
            background: white;
            color: #2563eb;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            font-weight: 600;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.4s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Results Styles tailored to Screenshot */
        .metric-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }

        .premium-receipt {
            background: white;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }

        .metric-row, .receipt-line {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f1f5f9;
            color: #334155;
        }
        
        .metric-row:last-child { border-bottom: none; }

        .receipt-sub {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: -8px;
            margin-bottom: 15px;
            font-style: italic;
        }
        
        .receipt-total {
            margin-top: 25px;
            padding-top: 25px;
            border-top: 1px dashed #cbd5e1;
            display: flex;
            justify-content: space-between;
            font-size: 1.4rem;
            font-weight: 700;
            color: #0f172a;
        }

        .metric-title { color: #64748b; font-weight: 500; }
        .metric-value { color: #1e293b; font-weight: 600; }
        
        .success-box {
            background: white;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #22c55e;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .risk-badge {
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .risk-HIGH { background: #fee2e2; color: #991b1b; }
        .risk-MEDIUM { background: #fef9c3; color: #854d0e; }
        .risk-LOW { background: #dcfce7; color: #166534; }

        .letter-content {
            white-space: pre-wrap;
            font-family: 'Times New Roman', serif;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #333;
            background: #fff;
            padding: 40px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .loading-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255,255,255,0.95);
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }
        
        .loading-overlay.active { display: flex; }
        
        .spinner {
            width: 40px; height: 40px;
            border: 4px solid #e2e8f0; border-top: 4px solid #2563eb;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>🏢 AI Insurance Underwriting</h1>
                <p>Advanced Orchestration with LangChain & Gemini (RAG)</p>
            </div>
        </div>

        <div class="main-content">
            <!-- Left Panel: Input -->
            <div class="panel">
                <div class="panel-header">
                    <h2>📥 Quote Request</h2>
                    <span style="font-size: 0.9rem; color: #64748b;">Processing Gateway</span>
                </div>
                <div class="panel-body" style="position: relative;">
                    <div class="input-group">
                        <label>Select Scenario</label>
                        <select id="scenarioSelect" onchange="loadScenario()">
                            <option value="construction">Construction Corp (Standard Demo)</option>
                            <option value="tech">Tech Startup (SaaS)</option>
                            <option value="restaurant">Gourmet Restaurant</option>
                            <option value="retail">Retail Store Chain</option>
                            <option value="custom">Custom Input...</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Email Content</label>
                        <textarea id="emailInput" placeholder="Paste email content here..."></textarea>
                    </div>

                    <button class="button" onclick="processQuote()" id="processBtn">
                        <span id="btnText">⚡ Process Quote</span>
                    </button>

                    <div class="loading-overlay" id="loading">
                        <div class="spinner"></div>
                        <p style="color: #334155; font-weight: 600;">Analyzing Risk Profile...</p>
                        <div id="loadingLog" style="font-size: 0.85rem; color: #64748b; margin-top: 10px;"></div>
                    </div>
                </div>
            </div>

            <!-- Right Panel: Output -->
            <div class="panel">
                <div class="panel-header">
                    <h2>📊 Underwriting Analysis</h2>
                </div>
                <div class="panel-body" id="resultsArea">
                    <!-- Default State -->
                    <div style="text-align: center; color: #94a3b8; margin-top: 100px;">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom: 15px; opacity: 0.5;">
                             <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                             <polyline points="14 2 14 8 20 8"></polyline>
                             <line x1="16" y1="13" x2="8" y2="13"></line>
                             <line x1="16" y1="17" x2="8" y2="17"></line>
                             <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                        <p>Waiting for quote request...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const scenarios = {
            construction: `Subject: Quote Request - ABC Construction Corp

Hi there,

I need a quote for ABC Construction Corp. They're a mid-size commercial construction company based in Texas, doing about $15M in annual revenue. They need General Liability coverage with $2M/$4M limits, plus Auto Liability for their fleet of 25 vehicles.

The company has been in business for 12 years, 85 employees. They've had two small workers comp claims in the past 3 years but nothing major. They're looking for coverage to start March 1st.

Thanks,
Sarah Johnson`,
            
            tech: `Subject: Coverage Request - CloudSync Technologies

Hi Insurance Team,

We're a SaaS company called CloudSync Technologies looking for our first commercial insurance package. Here are our details:

Company Info:
- Founded 3 years ago in Austin, Texas
- We develop cloud-based project management software
- Current ARR (annual recurring revenue): $4.5 million
- 35 employees, all W-2, mostly remote with a small office
- We handle customer data so cyber security is a priority

What we're looking for:
1. General Liability - standard limits
2. Professional Liability / E&O - we need this for our client contracts
3. Cyber Liability - at least $1M, preferably $2M
4. We have 3 company vehicles for sales team

Previous coverage: This is our first policy, previously relied on personal policies
Loss history: None

We're growing fast and want to make sure we're properly protected. Several of our enterprise clients are requiring proof of insurance in their contracts.

Timeline: Need this sorted within 2 weeks

Thanks,
Jennifer Chen
COO, CloudSync Technologies
jennifer@cloudsync.io`,
            
            restaurant: `Subject: Insurance Quote - Mario's Italian Kitchen

Hello,

I'm reaching out on behalf of Mario's Italian Kitchen, a family-owned restaurant in downtown Chicago. They've been serving the community for 8 years and are looking for a comprehensive insurance package.

Details:
- Full-service Italian restaurant
- Annual revenue: approximately $2.2 million
- 22 employees (mix of full-time and part-time)
- Square footage: 4,500 sq ft
- They have a full bar with liquor license (about 30% of revenue from alcohol)
- Open 7 days a week, 11am to 11pm
- No delivery service, dine-in and takeout only
- Building is leased, need tenant coverage
- Clean claims history - one slip and fall claim 4 years ago that was under $5,000

They need:
- General Liability ($1M/$2M)
- Property coverage for equipment and contents (approximately $350,000 value)
- Liquor Liability
- Workers Compensation

Hoping to have coverage in place by the 15th of next month for their lease renewal.

Best regards,
Michael Torres
Torres Insurance Agency`,

            retail: `Subject: Renewal Quote - Fashion Forward Boutique

Good morning,

I'm the owner of Fashion Forward Boutique and my current policy is coming up for renewal. I'd like to get a competitive quote.

About my business:
- Women's clothing and accessories retail store
- Located in a strip mall in suburban Atlanta, Georgia
- Been open for 6 years
- Annual sales around $850,000
- Just me and 4 part-time employees
- Store is 2,200 square feet, I lease the space
- Inventory value approximately $175,000
- No claims ever filed

Current coverage (looking for similar):
- General Liability $1M/$2M
- Business Personal Property
- Business Income coverage

I also have a small cargo van for picking up inventory from suppliers - would like to add that if possible.

My current premium is around $3,200/year and I'm hoping to stay in that range or lower if possible.

Renewal date is in 45 days.

Thank you,
Amanda Williams
Fashion Forward Boutique
(404) 555-0123`
        };

        function loadScenario() {
            const select = document.getElementById('scenarioSelect');
            const val = select.value;
            if (val !== 'custom') {
                document.getElementById('emailInput').value = scenarios[val];
            } else {
                document.getElementById('emailInput').value = "";
                document.getElementById('emailInput').focus();
            }
        }

        window.onload = function() { loadScenario(); };

        async function processQuote() {
            const emailContent = document.getElementById('emailInput').value;
            if (!emailContent.trim()) { alert('Please enter content'); return; }

            const loading = document.getElementById('loading');
            const log = document.getElementById('loadingLog');
            loading.classList.add('active');
            
            // Steps simulation
            const steps = ["Extracting Data...", "Retrieving Guidelines...", "Calculating Risk...", "Drafting Quote..."];
            let idx = 0;
            const iv = setInterval(() => { if(idx < steps.length) log.innerText = steps[idx++]; }, 800);

            try {
                const response = await fetch('/api/process-rag-quote', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ email_content: emailContent })
                });
                
                const result = await response.json();
                clearInterval(iv);
                
                if (result.success) {
                    displayResults(result.data);
                } else {
                    console.error("Server Error:", result);
                    alert('Analysis Failed: ' + (result.error || "Unknown Error"));
                }
            } catch (e) {
                clearInterval(iv);
                console.error("Network Error:", e);
                alert('Connection Error - Please ensure server is running');
            } finally {
                loading.classList.remove('active');
            }
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function displayResults(data) {
            try {
                const fmt = (v) => v ? '$' + v.toLocaleString('en-US', {minimumFractionDigits: 0}) : '$0';
                const fmt2 = (v) => v ? '$' + v.toLocaleString('en-US', {minimumFractionDigits: 2}) : '$0.00';

                // Ensure data fields exist to prevent rendering errors
                const industry = data.industry || "Unknown Industry";
                const risk = data.risk_level || "MEDIUM";
                const quoteId = data.quote_id || "PENDING";
                const client = data.client_name || "Client";
                
                // Safe Access for Calculation Details
                const calc = data.calculation_details || {};
                const glBase = calc.gl_base || 0;
                const glFormula = calc.gl_formula || "Base Rate";
                const lossMod = calc.loss_modifier || 0;
                const lossDesc = calc.loss_percent || "N/A";
                const lossFormula = calc.loss_formula || "";
                const autoPrem = calc.auto_premium || 0;
                const autoDesc = calc.auto_formula || "Auto/Other";
                const autoFormula = calc.auto_formula_desc || "";
                const totalPrem = data.final_premium || 0;

                const html = `
                    <div class="tabs">
                        <div class="tab active" onclick="switchTab('tab-summary')">Quote Summary</div>
                        <div class="tab" onclick="switchTab('tab-premium')">Premium Breakdown</div>
                        <div class="tab" onclick="switchTab('tab-risk')">Risk Assessment</div>
                        <div class="tab" onclick="switchTab('tab-letter')">Quoted Email</div>
                    </div>

                    <!-- Tab 1: Quote Summary -->
                    <div id="tab-summary" class="tab-content active">
                        <div class="success-box">
                            <h3 style="color: #22c55e; margin: 0; display: flex; align-items: center; gap: 10px;">
                                <span style="font-size: 1.2rem;">✅</span> Quote Generated Successfully
                            </h3>
                        </div>
                        
                        <div class="metric-row">
                            <span class="metric-title">Quote ID</span>
                            <span class="metric-value">${quoteId}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-title">Client Name</span>
                            <span class="metric-value">${client}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-title">Industry</span>
                            <span class="metric-value">${industry}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-title">Total Premium</span>
                            <span class="metric-value" style="color: #2563eb; font-size: 1.2rem;">${fmt2(totalPrem)}</span>
                        </div>
                    </div>

                    <!-- Tab 2: Breakdown -->
                    <div id="tab-premium" class="tab-content">
                        <div style="background: white; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0;">
                            <h3 style="font-size: 1.1rem; font-weight: 600; color: #334155; margin-bottom: 25px;">Premium Calculation</h3>
                            
                            <div style="margin-bottom: 8px;">
                                <div style="display: flex; justify-content: space-between; color: #334155; font-size: 1.05rem;">
                                    <span>- Base Premium (GL):</span>
                                    <span style="font-weight: 600;">$${glBase.toLocaleString()}</span>
                                </div>
                                ${glFormula ? `<div style="font-size: 0.85rem; color: #94a3b8; font-style: italic; margin-top: 4px; margin-bottom: 12px;">(${glFormula})</div>` : ''}
                            </div>

                            <div style="margin-bottom: 8px;">
                                <div style="display: flex; justify-content: space-between; color: #334155; font-size: 1.05rem;">
                                    <span>- ${lossDesc}:</span>
                                    <span style="font-weight: 600;">$${lossMod.toLocaleString()}</span>
                                </div>
                                ${lossFormula ? `<div style="font-size: 0.85rem; color: #94a3b8; font-style: italic; margin-top: 4px; margin-bottom: 12px;">(${lossFormula})</div>` : '<div style="margin-bottom: 12px;"></div>'}
                            </div>

                            <div style="margin-bottom: 8px;">
                                <div style="display: flex; justify-content: space-between; color: #334155; font-size: 1.05rem;">
                                    <span>- ${autoDesc}:</span>
                                    <span style="font-weight: 600;">$${autoPrem.toLocaleString()}</span>
                                </div>
                                ${autoFormula ? `<div style="font-size: 0.85rem; color: #94a3b8; font-style: italic; margin-top: 4px; margin-bottom: 12px;">(${autoFormula})</div>` : ''}
                            </div>

                            <div style="margin-top: 25px; padding-top: 20px; border-top: 1px dashed #cbd5e1; display: flex; justify-content: space-between; font-size: 1.4rem; font-weight: 700; color: #0f172a;">
                                <span>Total Annual Premium:</span>
                                <span>$${totalPrem.toLocaleString()}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Tab 3: Risk -->
                    <div id="tab-risk" class="tab-content">
                        <div class="metric-card">
                            <div class="metric-row">
                                <span class="metric-title">Risk Level</span>
                                <span class="risk-badge risk-${risk.toUpperCase()}">${risk}</span>
                            </div>
                            <div class="metric-row">
                                <span class="metric-title">Risk Score</span>
                                <span class="metric-value">${data.risk_score || 0}/100</span>
                            </div>
                            <div class="metric-row">
                                <span class="metric-title">Underwriting Authority</span>
                                <span class="metric-value">${data.authority || 'PENDING'}</span>
                            </div>
                        </div>
                        
                        <div class="metric-card">
                            <h4 style="margin-bottom: 10px;">Analysis</h4>
                            <p style="color: #64748b;">${data.coverage_analysis || "No analysis available."}</p>
                        </div>
                    </div>

                    <!-- Tab 4: Letter -->
                    <div id="tab-letter" class="tab-content">
                        <div class="letter-content">${data.quote_letter || "Quote letter generation failed."}</div>
                        <button class="button" style="margin-top: 20px;">
                            <span>Download Quote</span>
                        </button>
                    </div>
                `;
                
                document.getElementById('resultsArea').innerHTML = html;
            } catch (err) {
                console.error("Rendering Error", err);
                alert("Error displaying results: " + err.message);
            }
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🚀 AI INSURANCE UNDERWRITING | RAG ENGINE")
    print("="*70)
    print("\n✅ Server starting (Professional UI)...")
    print("👉 ACCESS HERE: http://localhost:8002")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
