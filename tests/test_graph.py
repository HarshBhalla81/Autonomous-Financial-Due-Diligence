import sys
import os
import json

# Add the root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.graph import DueDiligenceOrchestrator

def test_autonomous_flow():
    print("=== Starting End-to-End Autonomous Test ===")
    
    orchestrator = DueDiligenceOrchestrator()
    
    # Simulate user input from Streamlit
    sample_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_income_statement.csv")
    target = "AAPL"
    competitors = ["MSFT"]
    
    # Run the autonomous graph
    final_state = orchestrator.run_due_diligence(
        document_path=sample_file,
        target_symbol=target,
        competitors=competitors
    )
    
    print("\n=== Pipeline Execution Finished ===")
    print(f"Errors encountered: {final_state.get('errors')}")
    
    if not final_state.get('errors'):
        print("\nSuccess! The state contains:")
        print(f"- Parsed Document Tables: {len(final_state['parsed_document'].get('tables', []))} tables")
        
        metrics = final_state.get('financial_metrics', {})
        print(f"- Computed Gross Margins: {metrics.get('ratios', {}).get('2023', {}).get('Gross Margin (%)')}% (for 2023)")
        
        intel = final_state.get('market_intelligence', {})
        print(f"- Market Sector Average P/E: {intel.get('sector_benchmarks', {}).get('Average_PE_Ratio')}")
        
        print("\n\n" + "="*50)
        print("FINAL INVESTMENT MEMO:")
        print("="*50)
        print(final_state.get('final_memo', 'No memo generated.'))
        print("="*50)
        
if __name__ == "__main__":
    test_autonomous_flow()
