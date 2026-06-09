import sys
import os
from typing import List

# Ensure core module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.schemas import MarketIntelligence
from mcp_servers.financial_mcp import get_company_overview, get_global_quote

class MarketIntelligenceAgent:
    """
    The Market Intelligence Agent drives programmatic API collection loops to grab
    competitor valuation multiples and calculate sector benchmarks.
    It interfaces directly with the MCP tools.
    """
    
    def gather_intelligence(self, target_symbol: str, competitors: List[str]) -> MarketIntelligence:
        print(f"Market Intel Agent: Initiating data fetch for Target -> {target_symbol}")
        
        # 1. Fetch Target Data via MCP
        target_data = get_company_overview(target_symbol)
        
        # 2. Fetch Competitor Data via MCP
        comp_data = {}
        for comp in competitors:
            print(f"Market Intel Agent: Fetching competitor data -> {comp}")
            result = get_company_overview(comp)
            # Only keep successful API results to avoid corrupting benchmarks
            if "error" not in result:
                comp_data[comp] = result
            else:
                print(f"Warning: Failed to fetch data for {comp}. {result['error']}")
                
        # 3. Compute Sector Benchmarks (e.g., Average P/E Ratio, Average P/B Ratio)
        pe_ratios = []
        pb_ratios = []
        
        all_companies_data = [target_data] + list(comp_data.values())
        
        for data in all_companies_data:
            if "error" in data:
                continue
                
            pe = data.get("PERatio")
            pb = data.get("PriceToBookRatio")
            
            try:
                if pe and pe != "None":
                    pe_ratios.append(float(pe))
                if pb and pb != "None":
                    pb_ratios.append(float(pb))
            except ValueError:
                pass
                
        avg_pe = sum(pe_ratios) / len(pe_ratios) if pe_ratios else 0.0
        avg_pb = sum(pb_ratios) / len(pb_ratios) if pb_ratios else 0.0
        
        print(f"Market Intel Agent: Computed Sector Average P/E -> {round(avg_pe, 2)}x")
        
        return MarketIntelligence(
            target_symbol=target_symbol,
            target_metrics=target_data,
            competitor_metrics=comp_data,
            sector_benchmarks={
                "Average_PE_Ratio": round(avg_pe, 2),
                "Average_PB_Ratio": round(avg_pb, 2)
            },
            market_context=f"Analyzed {target_symbol} against {len(comp_data)} competitors."
        )

if __name__ == "__main__":
    agent = MarketIntelligenceAgent()
    print("Market Intelligence Agent loaded.")
