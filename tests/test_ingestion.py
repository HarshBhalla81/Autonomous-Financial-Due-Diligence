import os
import sys
import json

# Add the root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ingestion_agent import IngestionAgent

def test_ingestion():
    agent = IngestionAgent()
    sample_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_income_statement.csv")
    
    print(f"Testing ingestion with file: {sample_file}")
    
    try:
        parsed_doc = agent.process_file(sample_file)
        print("\n--- Parsed Document Result ---")
        print(f"Source File: {parsed_doc.source_file}")
        print(f"File Type: {parsed_doc.file_type}")
        print("Text Content:", parsed_doc.text_content)
        print("\nExtracted Tables (JSON format):")
        print(json.dumps(parsed_doc.tables, indent=2))
        
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    test_ingestion()
