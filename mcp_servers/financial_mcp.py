import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables (API keys)
load_dotenv()

# Initialize the MCP Server
mcp = FastMCP("FinancialData")

@mcp.tool()
def get_company_overview(symbol: str) -> dict:
    """
    Get company overview including sector, industry, market cap, and basic ratios.
    Uses Alpha Vantage API.
    """
    api_key = os.getenv("FINANCIAL_API_KEY")
    if not api_key or api_key == "your_key_here":
        return {"error": "Valid FINANCIAL_API_KEY not found in environment."}
    
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

@mcp.tool()
def get_global_quote(symbol: str) -> dict:
    """
    Get the latest price and volume information for a ticker symbol.
    Uses Alpha Vantage API.
    """
    api_key = os.getenv("FINANCIAL_API_KEY")
    if not api_key or api_key == "your_key_here":
        return {"error": "Valid FINANCIAL_API_KEY not found in environment."}
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

if __name__ == "__main__":
    # Run the server using standard input/output, which is how LangGraph/Clients will interact with it
    mcp.run(transport='stdio')
