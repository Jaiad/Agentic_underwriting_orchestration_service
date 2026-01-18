import os
import sys

# Add root to path
sys.path.append(os.getcwd())

from src.graph_pipeline.graph import build_graph

def generate_graph_image():
    print("Building Graph...")
    app = build_graph()
    
    print("Generating Graph Image...")
    try:
        # Get the graph object
        graph = app.get_graph()
        
        # Method 1: Try generating PNG (Requires internet to reach mermaid API usually, or local renderer)
        png_data = graph.draw_mermaid_png()
        
        output_file = "agentic_graph_diagram.png"
        with open(output_file, "wb") as f:
            f.write(png_data)
        
        print(f"SUCCESS! Graph visual saved to: {os.path.abspath(output_file)}")
        print("Please open this file to see your Human-in-the-Loop architecture.")
        
    except Exception as e:
        print(f"Could not generate PNG directly: {e}")
        # Fallback: Print Mermaid code
        print("\n--- MERMAID CODE (Paste into https://mermaid.live) ---")
        print(graph.draw_mermaid())
        print("------------------------------------------------------")

if __name__ == "__main__":
    generate_graph_image()
