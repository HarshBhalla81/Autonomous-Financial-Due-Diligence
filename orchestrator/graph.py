import sys
import os

# Ensure core module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from core.state import DueDiligenceState

# Import the agents we built in Week 1
from agents.ingestion_agent import IngestionAgent
from agents.analysis_agent import AnalysisAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.reporting_agents import RiskAssessmentAgent, MemoGeneratorAgent
from core.schemas import ParsedDocument

class DueDiligenceOrchestrator:
    def __init__(self):
        # Initialize our isolated agents
        self.ingestion_agent = IngestionAgent()
        self.analysis_agent = AnalysisAgent()
        self.market_agent = MarketIntelligenceAgent()
        self.risk_agent = RiskAssessmentAgent()
        self.memo_agent = MemoGeneratorAgent()
        
        # Build the graph
        self.graph = self._build_graph()
        
    def _build_graph(self):
        workflow = StateGraph(DueDiligenceState)
        
        # Add Nodes (Each agent gets a node on the assembly line)
        workflow.add_node("ingest_data", self._node_ingest)
        workflow.add_node("analyze_financials", self._node_analyze)
        workflow.add_node("gather_market_intel", self._node_market_intel)
        workflow.add_node("assess_risk", self._node_risk_assessment)
        workflow.add_node("generate_memo", self._node_memo)
        
        # Define the routing (Edges)
        workflow.set_entry_point("ingest_data")
        workflow.add_edge("ingest_data", "analyze_financials")
        workflow.add_edge("analyze_financials", "gather_market_intel")
        workflow.add_edge("gather_market_intel", "assess_risk")
        workflow.add_edge("assess_risk", "generate_memo")
        workflow.add_edge("generate_memo", END)
        
        # Compile the autonomous workflow
        return workflow.compile()
        
    # --- Node Definitions ---
    
    def _node_ingest(self, state: DueDiligenceState):
        print("\n[Node: Ingestion] -> Reading and normalizing file...")
        try:
            parsed_doc = self.ingestion_agent.process_file(state["document_path"])
            # Save the result to the shared whiteboard
            return {"parsed_document": parsed_doc.model_dump(), "errors": []}
        except Exception as e:
            return {"errors": [f"Ingestion failed: {str(e)}"]}
            
    def _node_analyze(self, state: DueDiligenceState):
        print("\n[Node: Analysis] -> Computing deterministic math...")
        if state.get("errors"):
            return state # Skip if previous node failed
            
        try:
            # Reconstruct the object from the dict state
            parsed_doc = ParsedDocument(**state["parsed_document"])
            metrics = self.analysis_agent.analyze(parsed_doc)
            return {"financial_metrics": metrics.model_dump()}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Analysis failed: {str(e)}"]}

    def _node_market_intel(self, state: DueDiligenceState):
        print("\n[Node: Market Intel] -> Fetching live API competitor data...")
        if state.get("errors"):
            return state
            
        try:
            intel = self.market_agent.gather_intelligence(
                target_symbol=state["target_symbol"],
                competitors=state["competitors"]
            )
            return {"market_intelligence": intel.model_dump()}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Market Intel failed: {str(e)}"]}
            
    def _node_risk_assessment(self, state: DueDiligenceState):
        print("\n[Node: Risk Assessment] -> LLM is evaluating risks...")
        if state.get("errors"):
            return state
            
        try:
            risk_text = self.risk_agent.assess_risk(
                metrics=state.get("financial_metrics", {}),
                market_intel=state.get("market_intelligence", {})
            )
            return {"risk_assessment": risk_text}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Risk Assessment failed: {str(e)}"]}
            
    def _node_memo(self, state: DueDiligenceState):
        print("\n[Node: Memo Generation] -> LLM is formatting the final report...")
        if state.get("errors"):
            return state
            
        try:
            memo_text = self.memo_agent.generate_memo(state_dict=state)
            return {"final_memo": memo_text}
        except Exception as e:
            return {"errors": state.get("errors", []) + [f"Memo Generation failed: {str(e)}"]}
            
    # --- Execution ---
    def run_due_diligence(self, document_path: str, target_symbol: str, competitors: List[str]):
        initial_state = DueDiligenceState(
            document_path=document_path,
            target_symbol=target_symbol,
            competitors=competitors,
            parsed_document=None,
            financial_metrics=None,
            market_intelligence=None,
            risk_assessment="",
            final_memo="",
            errors=[]
        )
        
        print(f"Starting Autonomous Due Diligence for {target_symbol}...")
        # This single invoke command runs the entire pipeline!
        final_state = self.graph.invoke(initial_state)
        return final_state

if __name__ == "__main__":
    # Simple test block
    orchestrator = DueDiligenceOrchestrator()
    print("LangGraph Orchestrator initialized successfully!")
