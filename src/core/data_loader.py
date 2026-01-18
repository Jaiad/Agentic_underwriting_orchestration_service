"""
Data Loader for RAG System.
Loads text and JSON files from the data directory and converts them to LangChain Documents.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from langchain_core.documents import Document

def load_documents(data_dir: str = "data") -> List[Document]:
    """
    Load documents from the data directory.
    Supports .txt and .json files.
    """
    path = Path(data_dir)
    if not path.exists():
        raise ValueError(f"Data directory '{data_dir}' not found.")

    docs = []

    # 1. Load Text Files
    for p in path.glob("*.txt"):
        try:
            content = p.read_text(encoding="utf-8")
            if content.strip():
                 docs.append(Document(
                    page_content=content, 
                    metadata={"source": str(p), "type": "text"}
                ))
        except Exception as e:
            print(f"Error loading {p}: {e}")

    # 2. Load and Flatten JSON Files (Crucial for existing data)
    for p in path.glob("*.json"):
        try:
            content = json.loads(p.read_text(encoding="utf-8"))
            
            # Strategy: Convert each item in a JSON list to a separate document
            # or convert the whole object to a string if it's a dict
            if isinstance(content, list):
                for i, item in enumerate(content):
                    text_content = json.dumps(item, indent=2)
                    docs.append(Document(
                        page_content=text_content,
                        metadata={"source": str(p), "type": "json_item", "index": i}
                    ))
            elif isinstance(content, dict):
                # Check for "mappings" or other large structures and split if possible
                # For now, dump the whole thing (splitter will handle it)
                text_content = json.dumps(content, indent=2)
                docs.append(Document(
                    page_content=text_content,
                    metadata={"source": str(p), "type": "json_file"}
                ))
                
        except Exception as e:
             print(f"Error loading {p}: {e}")

    return docs
