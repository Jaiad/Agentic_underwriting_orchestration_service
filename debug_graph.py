
import sys
import os
import traceback

# Add root to path
sys.path.append(os.getcwd())

from src.graph_pipeline.graph import build_graph

def debug():
    print("Building graph...")
    app = build_graph()
    
    print("Invoking graph...")
    inputs = {
        "input_email": "Subject: Quote Request - ABC Construction Corp\n\nHi there,\n\nI need a quote for ABC Construction Corp. They're a mid-size commercial construction company based in Texas, doing about $15M in annual revenue.",
        "quote_id": "DEBUG-001"
    }
    
    try:
        config = {"configurable": {"thread_id": "1"}}
        res = app.invoke(inputs, config=config)
        print("Success!")
        print(res.get("quote_letter"))
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    debug()
