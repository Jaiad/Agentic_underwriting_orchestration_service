"""
Professional Web UI for Agentic Underwriting System (LangGraph Edition).
Matches the legacy 'Regex Mode' UI style exactly.
"""

import os
import sys
import uuid
import json
import logging
import uvicorn
import traceback
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load env immediately
load_dotenv()

# Add root to path
sys.path.append(os.getcwd())

# Import Backend
from src.graph_pipeline.graph import build_graph
from src.core.ssl_handler import configure_ssl_handling

configure_ssl_handling()
logger = logging.getLogger(__name__)

# Initialize App & Graph
app = FastAPI(title="Agentic Underwriting AI")
graph_app = build_graph()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    email_content: str
    thread_id: str = None

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE

@app.post("/api/process-agentic-quote")
async def process_quote(req: AgentRequest):
    """Run the LangGraph Agent and return detailed execution metadata."""
    try:
        thread_id = req.thread_id or str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        print(f"🚀 Running Graph for Thread: {thread_id}")
        
        # Initial State
        initial_state = {
            "input_email": req.email_content,
            "quote_id": thread_id[:8]
        }
        
        # Invoke Graph
        final_state = graph_app.invoke(initial_state, config=config)
        
        # Determine status and routing path
        status = "COMPLETED"
        routing_path = []
        execution_insights = {
            "manual_review": {"required": False, "reason": None},
            "security_scan": {"passed": True, "flags": []}
        }
        
        # Analyze security
        security_flags = final_state.get("security_flags", [])
        if security_flags and len(security_flags) > 0:
            execution_insights["security_scan"]["flags"] = security_flags
            execution_insights["security_scan"]["passed"] = False
            status = "TERMINATED"
        
        # Analyze risk-based routing (HIL)
        risk = final_state.get("risk_assessment", {})
        if risk.get("level") == "HIGH":
            execution_insights["manual_review"]["required"] = True
            execution_insights["manual_review"]["reason"] = f"HIGH risk (Revenue: ${risk.get('revenue_factor', 0):,.0f})"
            status = "WAITING_APPROVAL"
        
        print(f"✅ Graph Finished. Status: {status}")
        
        # Check if we are paused at manual review (graph state check)
        next_nodes = list(graph_app.get_state(config).next)
        if "manual_review" in next_nodes:
             status = "WAITING_APPROVAL"
             
        # Format Data for UI
        response_data = {
           "status": status,
           "thread_id": thread_id,
           "extracted_data": final_state.get("extracted_data", {}),
           "calculation": final_state.get("calculation", {}),
           "quote_letter": final_state.get("quote_letter", ""),
           "risk": final_state.get("risk_assessment", {}),
           "execution_insights": execution_insights
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/approve-quote")
async def approve_quote(req: AgentRequest):
    """Resume the graph execution after manual approval."""
    try:
        thread_id = req.thread_id
        if not thread_id:
            return JSONResponse({"error": "Thread ID required"}, status_code=400)
            
        config = {"configurable": {"thread_id": thread_id}}
        
        print(f"👍 Approving Thread: {thread_id}")
        
        # 1. Update State to Approved
        graph_app.update_state(config, {"is_approved": True})
        
        # 2. Resume Graph
        final_state = graph_app.invoke(None, config=config)
        
        response_data = {
            "status": "APPROVED",
            "thread_id": thread_id,
            "extracted_data": final_state.get("extracted_data", {}),
            "calculation": final_state.get("calculation", {}),
            "quote_letter": final_state.get("quote_letter", ""),
            "risk": final_state.get("risk_assessment", {}),
            "execution_insights": {"manual_review": {"required": False, "reason": "Approved"}}
        }
        
        return JSONResponse(response_data)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


# ==========================================
# PROFESSIONAL UI TEMPLATE (MATCHING LEGACY)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Underwriter</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            padding: 20px;
            color: #1a1a1a;
            line-height: 1.6;
        }

        .container { max-width: 1400px; margin: 0 auto; }

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

        .header-content h1 { color: #2c3e50; font-size: 1.8rem; margin-bottom: 5px; font-weight: 700; }
        .header-content p { color: #64748b; font-size: 0.95rem; }

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

        .panel-header h2 { font-size: 1.1rem; font-weight: 600; color: #334155; }

        .panel-body { padding: 25px; flex-grow: 1; overflow-y: auto; position: relative; }

        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 8px; font-size: 0.9rem; color: #64748b; font-weight: 500; }

        select, textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            color: #334155;
            background-color: #f8fafc;
            outline: none;
            transition: all 0.2s;
        }
        
        textarea { height: 350px; font-family: 'Monaco', 'Menlo', monospace; resize: none; }
        select:hover, textarea:focus { border-color: #3b82f6; background-color: white; }

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
            display: flex; align-items: center; justify-content: center; gap: 10px;
            margin-top: auto;
        }
        .button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }
        .button:disabled { background: #94a3b8; cursor: not-allowed; transform: none; box-shadow: none; }
        
        .button.secondary { background: white; border: 1px solid #cbd5e1; color: #475569; }
        .button.approve { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }

        /* Tabs */
        .tabs { display: flex; gap: 5px; background: #f1f5f9; padding: 5px; border-radius: 10px; margin-bottom: 20px; }
        .tab { flex: 1; padding: 10px; text-align: center; cursor: pointer; border-radius: 8px; font-size: 0.9rem; font-weight: 500; color: #64748b; }
        .tab:hover { background: rgba(255, 255, 255, 0.5); color: #334155; }
        .tab.active { background: white; color: #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.05); font-weight: 600; }
        
        .tab-content { display: none; animation: fadeIn 0.3s ease; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

        /* Results */
        .metric-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .metric-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e2e8f0; }
        .metric-row:last-child { border-bottom: none; }
        .metric-title { color: #64748b; font-weight: 500; }
        .metric-value { color: #1e293b; font-weight: 600; }

        .premium-display { background: white; border-radius: 12px; padding: 25px; margin-top: 10px; border: 1px solid #e2e8f0; }
        .calc-line { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 0.95rem; color: #475569; }
        .calc-detail { font-size: 0.85rem; color: #94a3b8; margin-left: 10px; margin-top: 2px; font-style: italic; }
        .calc-total { margin-top: 20px; padding-top: 20px; border-top: 2px dashed #cbd5e1; display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: 700; color: #0f172a; }

        .risk-badge { padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
        .risk-low { background: #dcfce7; color: #166534; }
        .risk-medium { background: #fef9c3; color: #854d0e; }
        .risk-high { background: #fee2e2; color: #991b1b; }

        .letter-content { white-space: pre-wrap; font-family: 'Times New Roman', serif; font-size: 1.1rem; line-height: 1.6; color: #333; background: #fff; padding: 30px; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }

        .loading-overlay { position: absolute; inset: 0; background: rgba(255,255,255,0.95); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 10; }
        .loading-overlay.active { display: flex; }
        .spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top: 4px solid #3b82f6; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 15px; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

        .approval-alert {
            background: #fff1f2; border: 1px solid #fda4af; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;
        }
        .approval-alert h3 { color: #991b1b; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>🏢 Agentic AI Underwriting</h1>
                <p>Advanced Orchestration with Human-in-the-Loop</p>
            </div>
        </div>

        <div class="main-content">
            <!-- Left Panel -->
            <div class="panel">
                <div class="panel-header">
                    <h2>📥 Quote Request</h2>
                    <span style="font-size: 0.9rem; color: #64748b;">Processing Gateway</span>
                </div>
                <div class="panel-body">
                    <div class="input-group">
                        <label>Select Scenario</label>
                        <select id="scenarioSelect" onchange="loadScenario()">
                            <option value="construction">Construction Corp (Standard)</option>
                            <option value="construction_high">Construction Corp (Extreme Risk)</option>
                            <option value="retail">Retail Store Chain</option>
                            <option value="restaurant">Gourmet Restaurant</option>
                            <option value="tech">Tech Startup</option>
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
                        <p id="loadingText" style="color: #64748b; font-weight: 500;">Agents Working...</p>
                    </div>
                </div>
            </div>

            <!-- Right Panel -->
            <div class="panel">
                <div class="panel-header">
                    <h2>📊 Underwriting Analysis</h2>
                </div>
                <div class="panel-body" id="resultsArea">
                    <div style="text-align: center; color: #94a3b8; margin-top: 100px;">
                        <p>Waiting for quote request...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const scenarios = {
            construction: "Subject: Quote Request - ABC Construction Corp\\n\\nHi there,\\n\\nI need a quote for ABC Construction Corp. They're a mid-size commercial construction company based in Texas, doing about $15M in annual revenue. They need General Liability coverage with $2M/$4M limits, plus Auto Liability for their fleet of 25 vehicles.\\n\\nThe company has been in business for 12 years, 85 employees. They've had two small workers comp claims in the past 3 years but nothing major. They're looking for coverage to start March 1st.\\n\\nThis is somewhat urgent - they're shopping around and want to make a decision by end of week.\\n\\nThanks,\\nSarah Johnson\\nABC Insurance Brokerage",
            
            construction_high: "Subject: HIGH RISK QUOTE REQUEST - StructFail Corp\\n\\nURGENT: We need a quote for StructFail Corp.\\n\\nRisk Profile:\\n- 10 structural failures in last 2 years (major casualties)\\n- Handling hazardous nuclear waste without full permits\\n- 500 outstanding claims totaling $200M\\n- Safety Rating: F- (Lowest possible)\\n- filing for bankruptcy\\n\\nPlease approve immediately if possible.\\n\\nRevenue: $15M",

            retail: "Subject: Renewal Quote - Fashion Forward Boutique\\n\\nGood morning,\\n\\nI'm the owner of Fashion Forward Boutique and my current policy is coming up for renewal. I'd like to get a competitive quote.\\n\\nAbout my business:\\n- Women's clothing and accessories retail store\\n- Located in a strip mall in suburban Atlanta, Georgia\\n- Been open for 6 years\\n- Annual sales around $850,000\\n- Just me and 4 part-time employees\\n- Store is 2,200 square feet, I lease the space\\n- Inventory value approximately $175,000\\n- No claims ever filed\\n\\nCurrent coverage (looking for similar):\\n- General Liability $1M/$2M\\n- Business Personal Property\\n- Business Income coverage\\n\\nI also have a small cargo van for picking up inventory from suppliers - would like to add that if possible.\\n\\nMy current premium is around $3,200/year and I'm hoping to stay in that range or lower if possible.\\n\\nRenewal date is in 45 days.\\n\\nThank you,\\nAmanda Williams\\nFashion Forward Boutique\\n(404) 555-0123",
            
            restaurant: "Subject: Insurance Quote - Mario's Italian Kitchen\\n\\nHello,\\n\\nI'm reaching out on behalf of Mario's Italian Kitchen, a family-owned restaurant in downtown Chicago. They've been serving the community for 8 years and are looking for a comprehensive insurance package.\\n\\nDetails:\\n- Full-service Italian restaurant\\n- Annual revenue: approximately $2.2 million\\n- 22 employees (mix of full-time and part-time)\\n- Square footage: 4,500 sq ft\\n- They have a full bar with liquor license (about 30% of revenue from alcohol)\\n- Open 7 days a week, 11am to 11pm\\n- No delivery service, dine-in and takeout only\\n- Building is leased, need tenant coverage\\n- Clean claims history - one slip and fall claim 4 years ago that was under $5,000\\n\\nThey need:\\n- General Liability ($1M/$2M)\\n- Property coverage for equipment and contents (approximately $350,000 value)\\n- Liquor Liability\\n- Workers Compensation\\n\\nHoping to have coverage in place by the 15th of next month for their lease renewal.\\n\\nBest regards,\\nMichael Torres\\nTorres Insurance Agency",
            
            tech: "Subject: Coverage Request - CloudSync Technologies\\n\\nHi Insurance Team,\\n\\nWe're a SaaS company called CloudSync Technologies looking for our first commercial insurance package. Here are our details:\\n\\nCompany Info:\\n- Founded 3 years ago in Austin, Texas\\n- We develop cloud-based project management software\\n- Current ARR (annual recurring revenue): $4.5 million\\n- 35 employees, all W-2, mostly remote with a small office\\n- We handle customer data so cyber security is a priority\\n\\nWhat we're looking for:\\n1. General Liability - standard limits\\n2. Professional Liability / E&O - we need this for our client contracts\\n3. Cyber Liability - at least $1M, preferably $2M\\n4. We have 3 company vehicles for sales team\\n\\nPrevious coverage: This is our first policy, previously relied on personal policies\\nLoss history: None\\n\\nWe're growing fast and want to make sure we're properly protected. Several of our enterprise clients are requiring proof of insurance in their contracts.\\n\\nTimeline: Need this sorted within 2 weeks\\n\\nThanks,\\nJennifer Chen\\nCOO, CloudSync Technologies\\njennifer@cloudsync.io"
        };
        
        let currentThreadId = null;

        function loadScenario() {
            const val = document.getElementById('scenarioSelect').value;
            if(val !== 'custom') {
                document.getElementById('emailInput').value = scenarios[val];
            } else {
                document.getElementById('emailInput').value = "";
            }
        }
        window.onload = loadScenario;

        async function processQuote() {
            const email = document.getElementById('emailInput').value;
            if(!email) return alert("Please enter email");
            
            setLoading(true);
            
            try {
                const res = await fetch('/api/process-agentic-quote', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ email_content: email })
                });
                const data = await res.json();
                
                if(data.error) throw new Error(data.error);
                
                displayResults(data);
                
            } catch(e) {
                alert("Error: " + e.message);
            } finally {
                setLoading(false);
            }
        }
        
        async function approveQuote() {
            if(!currentThreadId) return;
            const btn = document.getElementById('approveBtn');
            btn.innerHTML = 'Approving...';
            btn.disabled = true;
            
            try {
                const res = await fetch('/api/approve-quote', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ email_content: "", thread_id: currentThreadId })
                });
                const data = await res.json();
                if(data.error) throw new Error(data.error);
                displayResults(data);
            } catch(e) {
                alert("Error: " + e.message);
                btn.innerHTML = '✅ Approve Quote';
                btn.disabled = false;
            }
        }

        function setLoading(active) {
            document.getElementById('loading').classList.toggle('active', active);
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function displayResults(data) {
            currentThreadId = data.thread_id;
            const ext = data.extracted_data || {};
            const calc = data.calculation || {};
            const risk = data.risk || {};
            
            const isApproved = data.status === "APPROVED" || data.status === "COMPLETED";
            const needsApproval = data.status === "WAITING_APPROVAL";

            let html = `
                <div class="tabs">
                    <div class="tab active" onclick="switchTab('tab-quote')">Quote Summary</div>
                    <div class="tab" onclick="switchTab('tab-premium')">Premium Breakdown</div>
                    <div class="tab" onclick="switchTab('tab-risk')">Risk Assessment</div>
                    <div class="tab" onclick="switchTab('tab-letter')">Quoted Email</div>
                </div>
            `;
            
            // Approval Alert
            if(needsApproval) {
                html += `
                    <div class="approval-alert">
                        <h3>🔴 Human-in-the-Loop Required</h3>
                        <p>High Risk profile detected. Underwriter approval required to proceed.</p>
                         <p style="margin-top:5px; font-weight:600;">Reason: ${data.execution_insights.manual_review.reason}</p>
                        <button class="button approve" id="approveBtn" onclick="approveQuote()" style="margin-top:15px; width:200px; margin-left:auto; margin-right:auto;">
                            ✅ Approve Quote
                        </button>
                    </div>
                `;
            }

            // Tab 1: Summary - MATCHING SCREENSHOT LAYOUT
            const quoteId = `Q-${ext.client_name ? ext.client_name.substring(0,3).toUpperCase() : 'UNK'}-2024-${Math.floor(Math.random() * 9000) + 1000}`;
            
            html += `
                <div id="tab-quote" class="tab-content active">
                    <div style="background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
                         ${needsApproval ? 
                            `<div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 25px;">
                                 <span style="font-size: 1.5rem; margin-right: 10px;">⚠️</span>
                                 <h2 style="color: #eab308; font-size: 1.4rem;">Analysis Paused</h2>
                            </div>` :
                            `<div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 25px;">
                                 <span style="font-size: 1.5rem; margin-right: 10px; color: #10b981;">✅</span>
                                 <h2 style="color: #3b82f6; font-size: 1.4rem;">Quote Generated Successfully</h2>
                            </div>`
                        }
                        
                        <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f1f5f9;">
                            <span style="color: #64748b; font-weight: 500;">Quote ID</span>
                            <span style="font-weight: 600; color: #1e293b;">${quoteId}</span>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f1f5f9;">
                            <span style="color: #64748b; font-weight: 500;">Client Name</span>
                            <span style="font-weight: 600; color: #1e293b;">${ext.client_name || '-'}</span>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f1f5f9;">
                            <span style="color: #64748b; font-weight: 500;">Industry</span>
                            <span style="font-weight: 600; color: #1e293b;">${ext.industry || '-'}</span>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; padding: 12px 0; margin-top: 10px;">
                            <span style="color: #64748b; font-weight: 500;">Total Premium</span>
                            <span style="color: #2563eb; font-size: 1.5rem; font-weight: 700;">
                                ${calc.final_premium ? '$'+calc.final_premium.toLocaleString(undefined, {minimumFractionDigits: 2}) : 'Pending'}
                            </span>
                        </div>
                    </div>
                </div>
            `;
            
            // Tab 2: Premium
            html += `
                <div id="tab-premium" class="tab-content">
                    <div class="premium-display">
                        <h3 style="margin-bottom: 20px; color: #334155;">Premium Calculation</h3>
                        <div class="calc-line">
                            <span><strong>- Base Premium (GL):</strong></span>
                            <span>$${(calc.gl_base||0).toLocaleString(undefined, {minimumFractionDigits:0})}</span>
                        </div>
                        <div class="calc-detail" style="margin-bottom: 15px;">(Based on ${calc.gl_formula || 'Standard Rate'})</div>
                        
                        <div class="calc-line">
                            <span><strong>- ${calc.loss_percent || 'Loss Modifier'}:</strong></span>
                            <span>$${(calc.loss_modifier||0).toLocaleString(undefined, {minimumFractionDigits:0})}</span>
                        </div>
                        
                        <div class="calc-line" style="margin-top: 15px;">
                            <span><strong>- ${calc.auto_formula_desc || 'Auto/Other Premium'}:</strong></span>
                            <span>$${(calc.auto_premium||0).toLocaleString(undefined, {minimumFractionDigits:0})}</span>
                        </div>
                        <div class="calc-detail">(${calc.auto_formula || 'Flat Rate'})</div>
                        
                        <div class="calc-total">
                            <span>Total Annual Premium:</span>
                            <span>$${(calc.final_premium||0).toLocaleString(undefined, {minimumFractionDigits:0})}</span>
                        </div>
                    </div>
                </div>
            `;
            
            // Tab 3: Risk
            const riskClass = (risk.level || 'LOW').toLowerCase();
            html += `
                <div id="tab-risk" class="tab-content">
                     <div class="metric-card">
                        <div class="metric-row">
                            <span class="metric-title">Risk Level</span>
                            <span class="risk-badge risk-${riskClass}">${risk.level || 'PENDING'}</span>
                        </div>
                        <div class="metric-row"><span class="metric-title">Risk Score</span><span class="metric-value">${risk.score || 0}/100</span></div>
                        <div class="metric-row"><span class="metric-title">Authority</span><span class="metric-value">${calc.authority || 'PENDING'}</span></div>
                    </div>
                    ${calc.coverage_analysis ? `
                        <div class="metric-card" style="margin-top: 15px;">
                            <h4 style="margin-bottom: 10px; color: #475569;">Coverage Analysis</h4>
                            <p style="color: #64748b; font-size: 0.95rem;">${calc.coverage_analysis}</p>
                        </div>
                    ` : ''}
                </div>
            `;
            
            // Tab 4: Letter
            html += `
                <div id="tab-letter" class="tab-content">
                    ${needsApproval ? 
                        '<p style="color:#d32f2f; text-align:center; padding:40px;">⚠️ Quote generation is paused pending Underwriter Approval.</p>' : 
                        `<div class="letter-content" style="margin-bottom: 20px;">${data.quote_letter || 'Compiling...'}</div>`
                    }
                </div>
            `;
            
            document.getElementById('resultsArea').innerHTML = html;
        }
    </script>
</body>
</html>
"""""

if __name__ == '__main__':
    print('🚀 Starting Agentic Web UI at http://localhost:8005 ...')
    uvicorn.run(app, host='127.0.0.1', port=8005)
