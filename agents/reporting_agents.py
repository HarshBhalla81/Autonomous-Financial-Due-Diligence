import os
import json
import sys
from dotenv import load_dotenv

# Ensure core module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

class RiskAssessmentAgent:
    """
    Consumes mathematically verified internal metrics and external market context
    to generate a written risk assessment using an LLM.
    """
    def __init__(self):
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("LLM_API_KEY")
        # Ensure fast/cheap testing using 3.5-turbo if 4o-mini is unavailable, but default to gpt-3.5-turbo
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key, temperature=0.2, max_retries=0)
        
    def assess_risk(self, metrics: dict, market_intel: dict) -> str:
        print("Risk Agent: Synthesizing financial and market risks...")
        from langchain_core.prompts import PromptTemplate
        
        prompt = PromptTemplate(
            template="""You are a senior financial due diligence analyst.
Based on the mathematically verified metrics and live market intelligence below, 
write a concise, 2-paragraph risk assessment. Highlight any shrinking margins, 
anomalies, or market valuation premiums/discounts. 
DO NOT hallucinate math. Only reference the numbers provided.

Financial Metrics:
{metrics}

Market Intelligence:
{market_intel}

Risk Assessment:""",
            input_variables=["metrics", "market_intel"]
        )
        chain = prompt | self.llm
        try:
            result = chain.invoke({
                "metrics": json.dumps(metrics, indent=2), 
                "market_intel": json.dumps(market_intel, indent=2)
            })
            return result.content
        except Exception as e:
            return f"Error generating Risk Assessment: {e}"


class MemoGeneratorAgent:
    """
    Consumes the entire assembled LangGraph state to draft the final markdown memo.
    """
    def __init__(self):
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("LLM_API_KEY")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key, temperature=0.3, max_retries=0)
        
    def generate_memo(self, state_dict: dict) -> str:
        print("Memo Agent: Drafting final investment memo...")
        from langchain_core.prompts import PromptTemplate
        
        prompt = PromptTemplate(
            template="""You are an elite investment banker. Write a final Due Diligence Investment Memo.
Use highly professional Markdown formatting.

Gathered Due Diligence State:
{state}

Strictly follow this structure:
# Investment Due Diligence Memo: {target_symbol}
## 1. Executive Summary
## 2. Financial Health (Ratios & Trends)
## 3. Market & Competitive Positioning
## 4. Risk Assessment
## 5. Final Recommendation
""",
            input_variables=["state", "target_symbol"]
        )
        chain = prompt | self.llm
        try:
            result = chain.invoke({
                "state": json.dumps(state_dict, indent=2), 
                "target_symbol": state_dict.get("target_symbol", "Target Company")
            })
            return result.content
        except Exception as e:
            return f"Error generating Memo: {e}"
