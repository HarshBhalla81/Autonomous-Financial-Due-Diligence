import sys
import os
import json

# Add the root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.market_intelligence_agent import MarketIntelligenceAgent

def test_market_intel():
    print("--- Running Market Intelligence Agent ---")
    agent = MarketIntelligenceAgent()
    
    # We will test with Apple as the target, and Microsoft & Google as competitors
    target = "AAPL"
    competitors = ["MSFT", "GOOGL"]
    
    try:
        intel = agent.gather_intelligence(target_symbol=target, competitors=competitors)
        
        print("\n--- Market Intelligence Results ---")
        print(f"Target: {intel.target_symbol}")
        print(f"Target P/E Ratio: {intel.target_metrics.get('PERatio', 'N/A')}")
        print(f"Sector Average P/E Ratio: {intel.sector_benchmarks.get('Average_PE_Ratio', 'N/A')}")
        
        # Simple analysis
        target_pe = float(intel.target_metrics.get('PERatio', 0))
        avg_pe = intel.sector_benchmarks.get('Average_PE_Ratio', 0)
        
        if target_pe > avg_pe:
            print(f"Insight: {target} is trading at a premium compared to its peers.")
        elif target_pe < avg_pe and target_pe > 0:
            print(f"Insight: {target} is trading at a discount compared to its peers.")
            
    except Exception as e:
        print(f"Error during market intel gathering: {e}")

if __name__ == "__main__":
    test_market_intel()
