import streamlit as st
import os
import sys

# Ensure root directory is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.graph import DueDiligenceOrchestrator

# Set page config for a professional look
st.set_page_config(page_title="Autonomous Financial DD", page_icon="📈", layout="wide")

st.title("📈 Autonomous Financial Due Diligence Platform")
st.markdown("""
This platform uses a multi-agent **LangGraph** orchestrator to compress weeks of financial due diligence into seconds. 
Upload a financial statement, define your target, and let the AI team gather the market context and draft the final memo.
""")

# Sidebar for inputs
with st.sidebar:
    st.header("Due Diligence Parameters")
    uploaded_file = st.file_uploader("Upload Target's Financials (CSV/PDF)", type=["csv", "pdf"])
    
    st.markdown("---")
    target_ticker = st.text_input("Target Ticker Symbol (e.g., AAPL)", "AAPL")
    competitors_str = st.text_input("Competitor Tickers (Comma separated)", "MSFT, GOOGL")
    
    st.markdown("---")
    run_btn = st.button("🚀 Run Due Diligence", type="primary", use_container_width=True)

# Main Execution Logic
if run_btn:
    if not uploaded_file:
        st.error("Please upload a financial document first to begin the pipeline.")
    else:
        # Save the uploaded file to the data directory temporarily
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        competitors = [c.strip() for c in competitors_str.split(",") if c.strip()]
        
        st.info(f"Initializing Multi-Agent Team for {target_ticker}...")
        
        # We use a spinner to show the user that the backend LangGraph is running
        with st.spinner("🤖 Agents are working: Ingesting Data -> Calculating Math -> Fetching Market Multiples -> Writing Memo..."):
            try:
                orchestrator = DueDiligenceOrchestrator()
                final_state = orchestrator.run_due_diligence(
                    document_path=file_path,
                    target_symbol=target_ticker,
                    competitors=competitors
                )
                
                # Check for errors in the LangGraph state
                if final_state.get("errors"):
                    st.warning("Pipeline finished, but some agents encountered issues:")
                    for err in final_state["errors"]:
                        st.write(f"- {err}")
                else:
                    st.success("✅ Due Diligence Completed Successfully!")
                
                # Display the results cleanly using Streamlit Tabs
                st.markdown("### Due Diligence Results")
                tab1, tab2, tab3 = st.tabs(["📝 Final Investment Memo", "📊 Financial Metrics", "🌍 Market Intelligence"])
                
                with tab1:
                    memo_content = final_state.get("final_memo", "")
                    if "Error generating Memo" in memo_content:
                        st.error(f"LLM Quota Error: Ensure your API key is funded. Raw output: {memo_content}")
                    else:
                        st.markdown(memo_content)
                    
                with tab2:
                    st.subheader("Mathematically Verified Outputs (Analysis Agent)")
                    st.json(final_state.get("financial_metrics", {}))
                    
                with tab3:
                    st.subheader("Live Market Benchmarks (Market Intel Agent)")
                    st.json(final_state.get("market_intelligence", {}))
                    
            except Exception as e:
                st.error(f"A critical error occurred: {e}")
