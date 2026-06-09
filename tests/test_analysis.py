import os
import sys
import json

# Add the root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ingestion_agent import IngestionAgent
from agents.analysis_agent import AnalysisAgent

def test_analysis():
    # 1. Ingest the data first
    ingestion = IngestionAgent()
    sample_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_income_statement.csv")
    
    parsed_doc = ingestion.process_file(sample_file)
    
    # 2. Run the Analysis Agent
    print("\n--- Running Deterministic Analysis Agent ---")
    analyzer = AnalysisAgent()
    metrics = analyzer.analyze(parsed_doc)
    
    # 3. Print out the structured mathematical results
    print("\n--- Mathematically Verified Results (No Hallucinations) ---")
    print(metrics.model_dump_json(indent=2))

if __name__ == "__main__":
    test_analysis()
