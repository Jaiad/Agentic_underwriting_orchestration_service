import requests
import json
import sys

def test_api():
    url = "http://127.0.0.1:8005/api/process-agentic-quote"
    
    # Test Case: Construction (High Risk)
    print("\n--- Testing High Risk Scenario (Construction) ---")
    payload = {
        "email_content": "Subject: Quote Request - ABC Construction Corp\n\nHi there,\n\nI need a quote for ABC Construction Corp. They're a mid-size commercial construction company based in Texas, doing about $15M in annual revenue. They need General Liability coverage with $2M/$4M limits, plus Auto Liability for their fleet of 25 vehicles.\n\nThe company has been in business for 12 years, 85 employees. They've had two small workers comp claims in the past 3 years but nothing major. They're looking for coverage to start March 1st.\n\nThis is somewhat urgent - they're shopping around and want to make a decision by end of week.\n\nThanks,\nSarah Johnson\nABC Insurance Brokerage"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Verify HIL
        print(f"Status: {data.get('status')}")
        manual_review = data.get('execution_insights', {}).get('manual_review', {})
        print(f"Manual Review Required: {manual_review.get('required')}")
        print(f"Reason: {manual_review.get('reason')}")
        
        if data.get('status') == "WAITING_APPROVAL":
            print("✅ HIL triggered correctly for High Risk.")
        else:
            print("❌ HIL FAILED to trigger.")

        # Verify Email Format (should be present even if waiting approval, or partially generated)
        # Note: In the current logic, if waiting approval, the quote letter might be empty or partial depending on implementation.
        # Let's check if the approval endpoint generates it correctly.
        
        thread_id = data.get('thread_id')
        if thread_id and data.get('status') == "WAITING_APPROVAL":
            print(f"\n--- Approving Quote for Thread {thread_id} ---")
            approve_url = "http://127.0.0.1:8005/api/approve-quote"
            approve_res = requests.post(approve_url, json={"thread_id": thread_id, "email_content": ""})
            approve_data = approve_res.json()
            
            letter = approve_data.get('quote_letter', '')
            print("\n--- Generated Quote Letter ---")
            print(letter[:200] + "...") # Print start
            
            # Verify specific phrases
            checks = [
                "Dear ABC Construction Corp",
                "QUOTE SUMMARY:",
                "Annual Premium: $",
                "Risk Assessment:",
                "Commercial Auto Coverage for your fleet"
            ]
            
            all_passed = True
            for check in checks:
                if check in letter:
                    print(f"✅ Found: '{check}'")
                else:
                    print(f"❌ MISSING: '{check}'")
                    all_passed = False
            
            if all_passed:
                print("✅ Email format matches requirements!")
            else:
                print("❌ Email format mismatch.")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
