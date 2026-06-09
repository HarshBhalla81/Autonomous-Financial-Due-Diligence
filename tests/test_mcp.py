import sys
import os

# Add the root directory to the python path so we can import the mcp_servers module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_servers.financial_mcp import get_company_overview, get_global_quote

def test_mcp_tools():
    print("Testing get_company_overview for AAPL...")
    overview = get_company_overview("AAPL")
    if "error" in overview:
        print("Error:", overview["error"])
    else:
        print(f"Success! AAPL Market Cap: {overview.get('MarketCapitalization', 'N/A')}")
        print(f"AAPL Sector: {overview.get('Sector', 'N/A')}")
        print(f"AAPL P/E Ratio: {overview.get('PERatio', 'N/A')}")
    
    print("\n---------------------------\n")
    
    print("Testing get_global_quote for MSFT...")
    quote = get_global_quote("MSFT")
    if "error" in quote:
        print("Error:", quote["error"])
    else:
        # Alpha Vantage returns data under the "Global Quote" key
        global_data = quote.get("Global Quote", {})
        print(f"Success! MSFT Current Price: {global_data.get('05. price', 'N/A')}")
        print(f"MSFT Trading Volume: {global_data.get('06. volume', 'N/A')}")

if __name__ == "__main__":
    test_mcp_tools()
