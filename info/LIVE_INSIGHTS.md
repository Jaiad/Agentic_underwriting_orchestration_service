# 🎯 LIVE EXECUTION INSIGHTS - Feature Documentation

## What's New

The Web UI now displays **REAL-TIME execution insights** showing which advanced patterns were actually triggered during graph execution!

---

## 📊 What You'll See in the UI

### Navigate to: http://localhost:8005

#### 1. **Quote Dashboard Tab**
Enhanced "Underwriter Notes" section now shows:
- ✅ **Normal execution** message
- 🔴 **MANUAL REVIEW REQUIRED** (if high-risk or high-premium)
- 🛡️ **SECURITY ALERT** (if PII detected)
- 📊 **Routing Path** (actual path taken through the graph)

**Example Outputs:**
```
Low Risk Scenario:
"Client TechStartup assessed as LOW Risk. Graph execution completed successfully.
📊 Routing Path:
Calculate → AUTO_QUOTE"

High Risk Scenario:
"Client MegaBuilder assessed as HIGH Risk.
🔴 MANUAL REVIEW REQUIRED:
HIGH risk (Revenue: $20,000,000)
📊 Routing Path:
Risk → MANUAL_REVIEW"
```

#### 2. **Agentic Intelligence Tab**
Now includes a **yellow "Live Execution Insights" box** showing:

**Conditional Routing:**
- ✅ TRIGGERED (when risk-based routing activated)
- ⬜ Not Used (when auto-approved)
- → Reason: Why routing was triggered
- → Path: Which path was taken (AUTO_APPROVE, MANUAL_REVIEW, EARLY_TERMINATION)

**Security Scan:**
- ✅ PASSED (no issues)
- 🛡️ FLAGGED (PII or injection detected)
- → Flags: List of detected issues

**Manual Review:**
- ✅ Auto-Approved (normal flow)
- 🔴 REQUIRED (needs human approval)
- → Reason: Why manual review is needed

**Fallback Chains:**
- ✅ Primary Succeeded (normal execution)
- 🔄 USED (fallback chain activated)
- → Details: Which fallback was used

#### 3. **Enhanced Metrics Display**
Security card now shows:
- **PASSED** (green) - Normal
- **FLAGGED** (red) - Security issues detected

---

## 🧪 Test Scenarios

### Scenario 1: Low Risk (Auto-Approve)
**Email:**
```
Subject: Quote for StartupCo
We are a small tech startup with $2M revenue.
Need GL coverage. 10 employees.
```

**Expected UI Output:**
- Dashboard Notes: "Graph execution completed successfully"
- Routing Path: "Calculate → AUTO_QUOTE"
- Live Insights:
  - Conditional Routing: ⬜ Not Used
  - Security Scan: ✅ PASSED
  - Manual Review: ✅ Auto-Approved
  - Fallback Chains: ✅ Primary Succeeded

---

### Scenario 2: High Risk (Manual Review)
**Email:**
```
Subject: Quote for MegaBuilder Corp
Commercial construction company, $20M annual revenue.
85 employees, 30 vehicles. Need GL and Auto.
```

**Expected UI Output:**
- Dashboard Notes: 
  ```
  🔴 MANUAL REVIEW REQUIRED:
  HIGH risk (Revenue: $20,000,000)
  📊 Routing Path:
  Risk → MANUAL_REVIEW
  ```
- Live Insights:
  - Conditional Routing: ✅ TRIGGERED
    - → Reason: High risk level detected
    - → Path: MANUAL_REVIEW
  - Security Scan: ✅ PASSED
  - Manual Review: 🔴 REQUIRED
    - → Reason: HIGH risk (Revenue: $20,000,000)
  - Fallback Chains: ✅ Primary Succeeded

---

### Scenario 3: High Premium (Manual Review)
**Email:**
```
Subject: Quote for Enterprise Corp
Large manufacturing company with $30M revenue.
200 employees, need comprehensive coverage.
```

**Expected UI Output:**
- Dashboard Notes:
  ```
  🔴 MANUAL REVIEW REQUIRED:
  Premium exceeds $100k ($145,675.00)
  📊 Routing Path:
  Calculate → MANUAL_REVIEW
  ```
- Live Insights:
  - Conditional Routing: ✅ TRIGGERED
    - → Reason: High premium amount
    - → Path: MANUAL_REVIEW
  - Manual Review: 🔴 REQUIRED
    - → Reason: Premium exceeds $100k ($145,675.00)

---

### Scenario 4: Security Issue (Early Termination)
**Email:**
```
Subject: Quote Request
My SSN is 123-45-6789 and my Credit Card is 4111-1111-1111-1111.
Need insurance for my business.
```

**Expected UI Output:**
- Dashboard Notes:
  ```
  🛡️ SECURITY ALERT:
  Flags detected: POTENTIAL_PII_SSN, POTENTIAL_PII_CC
  📊 Routing Path:
  Security → TERMINATED
  ```
- Security Card: **FLAGGED** (red)
- Live Insights:
  - Conditional Routing: ✅ TRIGGERED
    - → Reason: Security violation detected
    - → Path: EARLY_TERMINATION
  - Security Scan: 🛡️ FLAGGED
    - → Flags: POTENTIAL_PII_SSN, POTENTIAL_PII_CC

---

##  Backend Data Structure

The API now returns this additional data:

```json
{
  "status": "COMPLETED" | "WAITING_APPROVAL",
  "execution_insights": {
    "conditional_routing": {
      "triggered": true,
      "reason": "High risk level detected",
      "path_taken": "MANUAL_REVIEW"
    },
    "security_scan": {
      "flags_detected": ["POTENTIAL_PII_SSN"],
      "passed": false
    },
    "manual_review": {
      "required": true,
      "reason": "HIGH risk (Revenue: $20,000,000)"
    },
    "fallback_used": {
      "extraction": false,
      "details": "Primary extraction chain succeeded"
    }
  },
  "routing_path": [
    "Risk → MANUAL_REVIEW"
  ]
}
```

---

## 🎨 Visual Changes

### Before (Static):
- UI showed general information about patterns available
- No indication of which patterns were actually used
- No routing decisions visible

### After (Dynamic):
- ✅ Real-time display of triggered patterns
- ✅ Actual routing path visualization
- ✅ Security scan results
- ✅ Manual review status and reason
- ✅ Fallback chain usage tracking
- ✅ Color-coded status indicators

---

## 🔍 How It Works

### 1. **Backend Analysis** (`web_app_agentic.py`)
After graph execution, the backend:
- Analyzes `security_flags` in state
- Checks `risk_assessment.level`
- Evaluates `calculation.final_premium`
- Determines routing decisions
- Packages insights into `execution_insights` object

### 2. **Frontend Display** (JavaScript)
The UI:
- Receives `execution_insights` from API
- Dynamically generates "Live Execution Insights" box
- Updates dashboard notes with routing information
- Color-codes security status (green/red)
- Shows actual path taken through graph

### 3. **JSON Debug View**
Enhanced to include `execution_summary`:
```json
{
  "execution_summary": {
    "routing_triggered": true,
    "path_taken": "MANUAL_REVIEW",
    "security_passed": true,
    "manual_review_req": true,
    "fallback_used": false
  }
}
```

---

## ✨ Benefits

1. **Transparency**: See exactly which patterns were used
2. **Debugging**: Understand why certain decisions were made
3. **Demo-Ready**: Show off advanced features in action
4. **Audit Trail**: Track routing decisions for compliance
5. **Learning**: Understand how conditional routing works

---

## 🚀 Try It Now!

1. Start the web UI: `python web_app_agentic.py`
2. Go to: http://localhost:8005
3. Try different scenarios (low-risk, high-risk, PII)
4. Watch the "Live Execution Insights" update in real-time!

---

*The system now SHOWS you the advanced patterns in action, not just tells you about them!* 🎉
