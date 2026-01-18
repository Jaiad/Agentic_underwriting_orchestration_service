"""
Professional Web UI for Insurance Underwriting System
FastAPI + Modern HTML/CSS/JS Interface
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os

# CRITICAL: Import SSL handler FIRST
from src.core.ssl_handler import configure_ssl_handling
configure_ssl_handling()

# Set API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAMNfmzMDjUl4XncYBF2yEu_xvtJ-zkLzo'

# Use demo orchestrator for FAST web UI (< 1 second response)
# Full RAG pipeline available in terminal_demo.py (takes 30-60 seconds)
from langchain_orchestrator import UnderwritingOrchestrator

app = FastAPI(title="AI Insurance Underwriting Orchestrator")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize FAST orchestrator
print("="*70)
print("✅ Web UI initialized with Demo Orchestrator")
print("⚡ Instant responses for presentations")
print("💡 For full RAG/LangChain experience: python terminal_demo.py")
print("="*70)
orchestrator = UnderwritingOrchestrator()

class QuoteRequest(BaseModel):
    email_content: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main UI"""
    return HTML_TEMPLATE

class SaveRequest(BaseModel):
    quote_id: str
    content: str
    client: str

@app.post("/api/save-quote")
async def save_quote(request: SaveRequest):
    """Save quote to local file"""
    try:
        if not os.path.exists('output'):
            os.makedirs('output')
            
        filename = f"output/Quote_{request.client.replace(' ', '_')}_{request.quote_id}.txt"
        with open(filename, "w") as f:
            f.write(request.content)
            
        return JSONResponse(content={"success": True, "path": filename})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})

@app.post("/api/process-quote")
async def process_quote(request: QuoteRequest):
    """Process insurance quote using demo orchestrator (FAST)"""
    try:
        print(f"\n{'='*70}")
        print("📧 Processing quote request")
        print(f"{'='*70}\n")
        
        # Call demo orchestrator - instant response
        result = orchestrator.process_quote(request.email_content)
        
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
        print(f"{'='*70}\n")
        
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "model": "LangChain + Google Gemini"}

# Professional HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Insurance Underwriting Orchestrator</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
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
            justify-content: space-between;
            align-items: center;
        }

        .header-content h1 {
            color: #2c3e50;
            font-size: 1.8rem;
            margin-bottom: 5px;
            font-weight: 700;
        }

        .header-content p {
            color: #64748b;
            font-size: 0.95rem;
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: #e0f2fe;
            color: #0369a1;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #0ea5e9;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(14, 165, 233, 0); }
            100% { box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); }
        }

        .main-content {
            display: grid;
            grid-template-columns: 40% 60%;
            gap: 30px;
            height: calc(100vh - 180px);
            min-height: 600px;
        }

        .panel {
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            overflow: hidden;
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

        select:hover {
            border-color: #94a3b8;
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
            border-color: #3b82f6;
            background-color: white;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
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
            margin-top: auto;
        }

        .button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }

        .button:active {
            transform: translateY(0);
        }

        /* Tabs System */
        .tabs {
            display: flex;
            gap: 5px;
            background: #f1f5f9;
            padding: 5px;
            border-radius: 10px;
            margin-bottom: 20px;
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

        .tab:hover {
            background: rgba(255, 255, 255, 0.5);
            color: #334155;
        }

        .tab.active {
            background: white;
            color: #3b82f6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            font-weight: 600;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Results Styles */
        .metric-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }

        .metric-row:last-child {
            border-bottom: none;
        }

        .metric-title {
            color: #64748b;
            font-weight: 500;
        }

        .metric-value {
            color: #1e293b;
            font-weight: 600;
        }

        .premium-display {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-top: 10px;
            border: 1px solid #e2e8f0;
        }

        .calc-line {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            font-size: 0.95rem;
            color: #475569;
        }

        .calc-detail {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-left: 10px;
            margin-top: 2px;
            font-style: italic;
        }

        .calc-total {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px dashed #cbd5e1;
            display: flex;
            justify-content: space-between;
            font-size: 1.2rem;
            font-weight: 700;
            color: #0f172a;
        }

        .risk-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .risk-low { background: #dcfce7; color: #166534; }
        .risk-medium { background: #fef9c3; color: #854d0e; }
        .risk-high { background: #fee2e2; color: #991b1b; }

        .letter-content {
            white-space: pre-wrap;
            font-family: 'Times New Roman', serif;
            font-size: 1.1rem;
            line-height: 1.6;
            color: #333;
            background: #fff;
            padding: 30px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }

        .loading-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.9);
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
        }
        
        .loading-overlay.active { display: flex; }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #e2e8f0;
            border-top: 4px solid #3b82f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

    </style>
</head>
<body>
    <div class="container">
        <div class="header" style="justify-content: center; text-align: center;">
            <div class="header-content">
                <h1>🏢 AI Insurance Underwriting</h1>
                <p>Advanced Orchestration with LangChain & Gemini</p>
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
                            <option value="retail">Retail Store Chain</option>
                            <option value="restaurant">Gourmet Restaurant</option>
                            <option value="tech">Tech Startup (SaaS)</option>
                            <option value="custom">Custom Input...</option>
                        </select>
                    </div>

                    <div class="input-group">
                        <label>Email Content</label>
                        <textarea id="emailInput"></textarea>
                    </div>

                    <button class="button" onclick="processQuote()" id="processBtn">
                        <span>⚡ Process Quote</span>
                    </button>

                    <div class="loading-overlay" id="loading">
                        <div class="spinner"></div>
                        <p style="color: #64748b; font-weight: 500;">Analyzing Risk Profile...</p>
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
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" style="margin-bottom: 15px;">
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
            construction: "Subject: Quote Request - ABC Construction Corp\\n\\nHi there,\\n\\nI need a quote for ABC Construction Corp. They're a mid-size commercial construction company based in Texas, doing about $15M in annual revenue. They need General Liability coverage with $2M/$4M limits, plus Auto Liability for their fleet of 25 vehicles.\\n\\nThe company has been in business for 12 years, 85 employees. They've had two small workers comp claims in the past 3 years but nothing major. They're looking for coverage to start March 1st.\\n\\nThis is somewhat urgent - they're shopping around and want to make a decision by end of week.\\n\\nThanks,\\nSarah Johnson\\nABC Insurance Brokerage",
            
            retail: "Subject: Renewal Quote - Fashion Forward Boutique\\n\\nGood morning,\\n\\nI'm the owner of Fashion Forward Boutique and my current policy is coming up for renewal. I'd like to get a competitive quote.\\n\\nAbout my business:\\n- Women's clothing and accessories retail store\\n- Located in a strip mall in suburban Atlanta, Georgia\\n- Been open for 6 years\\n- Annual sales around $850,000\\n- Just me and 4 part-time employees\\n- Store is 2,200 square feet, I lease the space\\n- Inventory value approximately $175,000\\n- No claims ever filed\\n\\nCurrent coverage (looking for similar):\\n- General Liability $1M/$2M\\n- Business Personal Property\\n- Business Income coverage\\n\\nI also have a small cargo van for picking up inventory from suppliers - would like to add that if possible.\\n\\nMy current premium is around $3,200/year and I'm hoping to stay in that range or lower if possible.\\n\\nRenewal date is in 45 days.\\n\\nThank you,\\nAmanda Williams\\nFashion Forward Boutique\\n(404) 555-0123",
            
            restaurant: "Subject: Insurance Quote - Mario's Italian Kitchen\\n\\nHello,\\n\\nI'm reaching out on behalf of Mario's Italian Kitchen, a family-owned restaurant in downtown Chicago. They've been serving the community for 8 years and are looking for a comprehensive insurance package.\\n\\nDetails:\\n- Full-service Italian restaurant\\n- Annual revenue: approximately $2.2 million\\n- 22 employees (mix of full-time and part-time)\\n- Square footage: 4,500 sq ft\\n- They have a full bar with liquor license (about 30% of revenue from alcohol)\\n- Open 7 days a week, 11am to 11pm\\n- No delivery service, dine-in and takeout only\\n- Building is leased, need tenant coverage\\n- Clean claims history - one slip and fall claim 4 years ago that was under $5,000\\n\\nThey need:\\n- General Liability ($1M/$2M)\\n- Property coverage for equipment and contents (approximately $350,000 value)\\n- Liquor Liability\\n- Workers Compensation\\n\\nHoping to have coverage in place by the 15th of next month for their lease renewal.\\n\\nBest regards,\\nMichael Torres\\nTorres Insurance Agency",
            
            tech: "Subject: Coverage Request - CloudSync Technologies\\n\\nHi Insurance Team,\\n\\nWe're a SaaS company called CloudSync Technologies looking for our first commercial insurance package. Here are our details:\\n\\nCompany Info:\\n- Founded 3 years ago in Austin, Texas\\n- We develop cloud-based project management software\\n- Current ARR (annual recurring revenue): $4.5 million\\n- 35 employees, all W-2, mostly remote with a small office\\n- We handle customer data so cyber security is a priority\\n\\nWhat we're looking for:\\n1. General Liability - standard limits\\n2. Professional Liability / E&O - we need this for our client contracts\\n3. Cyber Liability - at least $1M, preferably $2M\\n4. We have 3 company vehicles for sales team\\n\\nPrevious coverage: This is our first policy, previously relied on personal policies\\nLoss history: None\\n\\nWe're growing fast and want to make sure we're properly protected. Several of our enterprise clients are requiring proof of insurance in their contracts.\\n\\nTimeline: Need this sorted within 2 weeks\\n\\nThanks,\\nJennifer Chen\\nCOO, CloudSync Technologies\\njennifer@cloudsync.io"
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

        // Initialize with default
        window.onload = function() {
            loadScenario();
        };

        let currentQuoteData = null;

        async function processQuote() {
            const emailContent = document.getElementById('emailInput').value;
            if (!emailContent.trim()) { alert('Please enter content'); return; }

            document.getElementById('loading').classList.add('active');
            
            try {
                const response = await fetch('/api/process-quote', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ email_content: emailContent })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    currentQuoteData = result.data;
                    displayResults(result.data);
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (e) {
                alert('Connection error');
            } finally {
                document.getElementById('loading').classList.remove('active');
            }
        }
        
        async function saveQuote() {
            if (!currentQuoteData) return;
            
            const btn = document.getElementById('saveBtn');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span>💾 Saving...</span>';
            
            try {
                const response = await fetch('/api/save-quote', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        quote_id: currentQuoteData.quote_id,
                        content: currentQuoteData.quote_letter,
                        client: currentQuoteData.client_name
                    })
                });
                const res = await response.json();
                if (res.success) {
                    alert('Quote saved successfully to: ' + res.path);
                } else {
                    alert('Error saving quote');
                }
            } catch (e) {
                alert('Connection error saving quote');
            } finally {
                btn.innerHTML = originalText;
            }
        }

        function switchTab(tabId) {
            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function displayResults(data) {
            const resultHtml = `
                <div class="tabs">
                    <div class="tab active" onclick="switchTab('tab-quote')">Quote Summary</div>
                    <div class="tab" onclick="switchTab('tab-premium')">Premium Breakdown</div>
                    <div class="tab" onclick="switchTab('tab-risk')">Risk Assessment</div>
                    <div class="tab" onclick="switchTab('tab-letter')">Quoted Email</div>
                </div>

                <!-- Tab 1: Quote Summary -->
                <div id="tab-quote" class="tab-content active">
                    <div class="metric-card" style="border-left: 4px solid #3b82f6;">
                        <h3 style="color: #3b82f6; margin-bottom: 15px;">✅ Quote Generated Successfully</h3>
                        <div class="metric-row">
                            <span class="metric-title">Quote ID</span>
                            <span class="metric-value">${data.quote_id}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-title">Client Name</span>
                            <span class="metric-value">${data.client_name}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-title">Industry</span>
                            <span class="metric-value">${data.industry}</span>
                        </div>
                         <div class="metric-row">
                            <span class="metric-title">Total Premium</span>
                            <span class="metric-value" style="font-size: 1.1em; color: #2563eb;">$${data.final_premium.toLocaleString('en-US', {minimumFractionDigits: 2})}</span>
                        </div>
                    </div>
                </div>

                <!-- Tab 2: Premium Breakdown -->
                <div id="tab-premium" class="tab-content">
                    <div class="premium-display">
                        <h3 style="margin-bottom: 20px; color: #334155;">Premium Calculation</h3>
                        
                        ${data.calculation_details ? `
                            <div class="calc-line">
                                <span><strong>- Base Premium (GL):</strong></span>
                                <span>$${data.calculation_details.gl_base.toLocaleString('en-US', {minimumFractionDigits: 0})}</span>
                            </div>
                            <div class="calc-detail" style="margin-bottom: 15px;">
                                (Based on ${data.calculation_details.gl_formula})
                            </div>

                            <div class="calc-line">
                                <span><strong>- ${data.calculation_details.loss_percent || 'Loss Modifier'}:</strong></span>
                                <span>$${data.calculation_details.loss_modifier.toLocaleString('en-US', {minimumFractionDigits: 0})}</span>
                            </div>

                            <div class="calc-line" style="margin-top: 15px;">
                                <span><strong>- Auto/Other Premium:</strong></span>
                                <span>$${data.calculation_details.auto_premium.toLocaleString('en-US', {minimumFractionDigits: 0})}</span>
                            </div>
                            <div class="calc-detail">
                                (${data.calculation_details.auto_formula})
                            </div>

                            <div class="calc-total">
                                <span>Total Annual Premium:</span>
                                <span>$${data.calculation_details.total.toLocaleString('en-US', {minimumFractionDigits: 0})}</span>
                            </div>
                        ` : `
                            <div class="calc-line">
                                <span>Base Premium</span>
                                <span>$${data.base_premium.toLocaleString('en-US')}</span>
                            </div>
                            <div class="calc-line">
                                <span>Total</span>
                                <span>$${data.final_premium.toLocaleString('en-US')}</span>
                            </div>
                        `}
                    </div>
                </div>

                <!-- Tab 3: Risk Assessment -->
                <div id="tab-risk" class="tab-content">
                    <div class="metric-card">
                        <div class="metric-row">
                            <span class="metric-title">Risk Level</span>
                            <span class="risk-badge risk-${data.risk_level.toLowerCase()}">${data.risk_level}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-title">Risk Score</span>
                            <span class="metric-value">${data.risk_score}/100</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-title">Underwriting Authority</span>
                            <span class="metric-value">${data.authority}</span>
                        </div>
                    </div>
                    <div class="metric-card" style="margin-top: 15px;">
                        <h4 style="margin-bottom: 10px; color: #475569;">Analysis</h4>
                        <p style="color: #64748b; font-size: 0.95rem; line-height: 1.5;">
                            ${data.coverage_analysis}
                        </p>
                    </div>
                </div>

                <!-- Tab 4: Quoted Email (Renamed from Quote Letter) -->
                <div id="tab-letter" class="tab-content">
                    <div class="letter-content" style="margin-bottom: 20px;">${data.quote_letter}</div>
                    <button class="button secondary" onclick="saveQuote()" id="saveBtn" style="width: 100%;">
                        <span>📥 Download Quote</span>
                    </button>
                </div>
            `;
            
            document.getElementById('resultsArea').innerHTML = resultHtml;
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🚀 AI INSURANCE UNDERWRITING ORCHESTRATOR")
    print("="*70)
    print("\n✅ Server starting...")
    print("📊 Model: LangChain + Google Gemini (gemini-1.5-flash)")
    print("\n🌐 Access the application at:")
    print("\n   👉 http://localhost:8000")
    print("   👉 http://127.0.0.1:8000")
    print("\n💡 Share this URL with your team to present the model!")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
