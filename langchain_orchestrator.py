"""
Simplified Demo Version - Works Without API Calls
Perfect for presentations when network/proxy issues exist
"""

import os
from typing import Dict, Any
import random

class UnderwritingOrchestrator:
    """Demo Underwriting System - No API calls needed"""
    
    def __init__(self):
        print("✅ Demo Orchestrator initialized (offline mode)")
        
    def process_quote(self, email_content: str) -> Dict[str, Any]:
        """Process insurance quote - Demo version - FAST MODE"""
        
        # Logic Router based on Email Content
        email_data = self._parse_email_demo(email_content)
        industry_type = email_data.get('industry_key', 'general')
        
        # Default values
        calc_details = None
        final_premium = 0
        
        if industry_type == "construction":
            # Construction Logic (Existing)
            revenue = 15000000
            rate_per_1000 = 8.50
            gl_base = (revenue / 1000) * rate_per_1000  # 127,500
            loss_mod = gl_base * 0.15                   # 19,125
            auto_prem = 25 * 750                        # 18,750
            final_premium = gl_base + loss_mod + auto_prem
            
            calc_details = {
                'gl_base': gl_base,
                'gl_formula': f"${revenue:,.0f} revenue ÷ $1,000 × ${rate_per_1000:.2f}",
                'loss_modifier': loss_mod,
                'loss_percent': "+15%",
                'auto_premium': auto_prem,
                'auto_formula': "25 vehicles × $750 base rate",
                'total': final_premium
            }

        elif industry_type == "restaurant":
            # Restaurant Logic ($2.2M Rev)
            revenue = 2200000
            gl_base = (revenue / 1000) * 5.50          # 12,100
            property_cov = 350000 * 0.02               # 7,000 (Equip/Contents)
            liquor_liab = revenue * 0.30 * 0.008       # 5,280 (30% alcohol sales)
            final_premium = gl_base + property_cov + liquor_liab
            
            calc_details = {
                'gl_base': gl_base,
                'gl_formula': f"${revenue:,.0f} revenue ÷ $1,000 × $5.50",
                'loss_modifier': property_cov,
                'loss_percent': "Property", # Repurposing field for display
                'auto_premium': liquor_liab,
                'auto_formula': "Liquor Liability (30% of Rev)",
                'total': final_premium
            }

        elif industry_type == "retail":
            # Retail Logic ($850k Rev)
            revenue = 850000
            gl_base = 650                               # Minimum Base
            property_cov = 175000 * 0.015               # 2,625 (Inventory)
            biz_income = revenue * 0.005                # 4,250
            final_premium = gl_base + property_cov + biz_income
            
            calc_details = {
                'gl_base': gl_base,
                'gl_formula': "Minimum Base Premium",
                'loss_modifier': property_cov,
                'loss_percent': "Property/Inventory",
                'auto_premium': biz_income,
                'auto_formula': "Business Income Coverage",
                'total': final_premium
            }

        elif industry_type == "tech":
            # Tech Startup Logic ($4.5M Rev)
            revenue = 4500000
            gl_base = 500                               # Low GL exposure
            cyber = 3500                                # Base Cyber
            e_and_o = revenue * 0.002                   # 9,000
            final_premium = gl_base + cyber + e_and_o
            
            calc_details = {
                'gl_base': gl_base,
                'gl_formula': "Standard Office GL",
                'loss_modifier': cyber,
                'loss_percent': "Cyber Security",
                'auto_premium': e_and_o,
                'auto_formula': "Professional Liability (E&O)",
                'total': final_premium
            }
            
        else:
            # Fallback
            revenue = 1000000
            final_premium = 5000
            calc_details = None

        industry = email_data.get('industry', 'General Business')
        calculation_details = calc_details

        authority = "APPROVED" if final_premium < 200000 else "REQUIRES_REVIEW"
        coverage = "Comprehensive coverage package tailored to industry risks."
        
        # Risk Scoring
        if industry_type == "construction":
            risk_score = 65
            risk_level = "HIGH"
        elif industry_type == "restaurant":
            risk_score = 45
            risk_level = "MEDIUM"
        else:
            risk_score = 25
            risk_level = "LOW"
        
        quote_letter = self._generate_demo_letter(email_data, industry, final_premium, risk_level)
        
        return {
            'client_name': email_data.get('client_name', 'Valued Client'),
            'industry': industry,
            'revenue': email_data.get('revenue', revenue),
            'base_premium': 0, # Not used in new display
            'modifiers': {},
            'final_premium': final_premium,
            'calculation_details': calculation_details,
            'authority': authority,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'coverage_analysis': coverage,
            'quote_letter': quote_letter,
            'quote_id': f"Q-{email_data.get('client_name', 'ABC')[:3].upper()}-2024-{random.randint(1000,9999)}"
        }
    
    def _parse_email_demo(self, email_content: str) -> Dict[str, Any]:
        """Demo email parser - extracts basic info"""
        import re
        content = email_content.lower()
        
        # Regex for Revenue (simple extraction of $X.X million or $XXX,XXX)
        revenue = 1000000
        rev_match = re.search(r'\$(\d+(?:\.\d+)?)\s*(million|m)', content)
        if rev_match:
            val = float(rev_match.group(1))
            if 'million' in rev_match.group(2) or 'm' in rev_match.group(2):
                revenue = int(val * 1000000)
        else:
            # Try finding $XXX,XXX pattern
            rev_match_k = re.search(r'\$([\d,]+)', content)
            if rev_match_k:
                val_str = rev_match_k.group(1).replace(',', '')
                if val_str.isdigit() and len(val_str) > 3:
                     revenue = int(val_str)

        # Regex for Employees
        employees = 10
        emp_match = re.search(r'(\d+)\s+employees', content)
        if emp_match:
             employees = int(emp_match.group(1))
        
        if "construction" in content or "15m" in content:
            return {
                'industry_key': 'construction',
                'client_name': "ABC Construction Corp",
                'industry': "Construction - Commercial (BIC: 0044)",
                'revenue': revenue
            }
        elif "restaurant" in content or "italian" in content:
            return {
                'industry_key': 'restaurant',
                'client_name': "Mario's Italian Kitchen",
                'industry': "Restaurant - Fine Dining",
                'revenue': revenue
            }
        elif "retail" in content or "clothing" in content:
            return {
                'industry_key': 'retail',
                'client_name': "Fashion Forward Boutique",
                'industry': "Retail - Clothing Store",
                'revenue': revenue
            }
        elif "tech" in content or "saas" in content or "software" in content:
            return {
                'industry_key': 'tech',
                'client_name': "CloudSync Technologies",
                'industry': "Technology - SaaS Provider",
                'revenue': revenue
            }
            
        return {
            'industry_key': 'general',
            'client_name': "Valued Client",
            'industry': "General Business",
            'revenue': revenue
        }
    
    def _generate_demo_letter(self, email_data: Dict, industry: str, premium: float, risk_level: str) -> str:
        """Generate demo quote letter"""
        client_name = email_data.get('client_name', 'Valued Client')
        
        letter = f"""Dear {client_name},

Thank you for your interest in our insurance services. We are pleased to present you with a comprehensive insurance quote tailored to your business needs.

QUOTE SUMMARY:
Industry Classification: {industry}
Annual Premium: ${premium:,.2f}
Risk Assessment: {risk_level}

Our underwriting team has carefully reviewed your submission and determined that your business profile aligns well with our coverage standards. The quoted premium reflects current market conditions and your specific risk factors.

COVERAGE HIGHLIGHTS:
• General Liability Coverage with competitive limits
• Commercial Auto Coverage for your fleet
• Professional risk management support
• 24/7 claims assistance

NEXT STEPS:
To proceed with this quote, please contact our team within 30 days. We're committed to providing you with exceptional service and comprehensive protection for your business.

We appreciate the opportunity to serve your insurance needs and look forward to partnering with you.

Best regards,
AI Underwriting Team
Insurance Solutions Division

Quote Reference: {email_data.get('client_name', 'ABC')[:3].upper()}-{random.randint(1000,9999)}
Valid Until: 30 days from issue date"""
        
        return letter

# Test if run directly
if __name__ == "__main__":
    orchestrator = UnderwritingOrchestrator()
    
    sample_email = """
Subject: Quote Request - ABC Construction Corp

Hi,

I need a quote for ABC Construction Corp. They are a commercial construction 
company in Texas with $15M revenue and 85 employees. They need General Liability 
$2M/$4M and Auto for 25 vehicles.

Thanks,
Sarah
"""
    
    print("\n" + "="*70)
    print("  INSURANCE QUOTE PROCESSING (DEMO MODE)")
    print("="*70 + "\n")
    print("Processing quote request...\n")
    
    result = orchestrator.process_quote(sample_email)
    
    print("\n" + "="*70)
    print("  QUOTE GENERATED SUCCESSFULLY")
    print("="*70 + "\n")
    print(f"Client: {result['client_name']}")
    print(f"Industry: {result['industry']}")
    print(f"\nAnnual Premium: ${result['final_premium']:,.2f}")
    
    if result.get('calculation_details'):
        det = result['calculation_details']
        print(f"\nPremium Calculation Breakdown:")
        print(f"  - Base Premium (GL): ${det['gl_base']:,.2f}")
        print(f"    ({det['gl_formula']} - BIC Code 44)")
        print(f"  - Loss History Modifier: {det['loss_percent']} (${det['loss_modifier']:,.2f})")
        print(f"  - Auto Liability Premium: ${det['auto_premium']:,.2f}")
        print(f"    ({det['auto_formula']})")
        print(f"  - Total Annual Premium: ${det['total']:,.2f}")

    print(f"\nRisk Assessment:")
    print(f"  Level: {result['risk_level']}")
    print(f"  Score: {result['risk_score']}/100")
    print(f"\nQuote ID: {result['quote_id']}")
    
    print("\n" + "="*70)
    print("Press Ctrl+C to exit...")
    try:
        while True:
            pass # Keep alive
    except KeyboardInterrupt:
        print("\nExiting...")
