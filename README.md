# Autonomous Financial Due Diligence Platform

An autonomous multi-agent system designed to compress the financial due diligence process from weeks to hours using LangGraph and Streamlit.

## Features
- **Multi-Agent Architecture**: 5 distinct agents handling Ingestion, Analysis, Risk Assessment, Market Intelligence, and Memo Generation.
- **Deterministic Math**: Python-based hard-coded calculations to avoid LLM mathematical hallucination.
- **MCP Integration**: Uses the Model Context Protocol to fetch external financial data.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```
   LLM_API_KEY=your_key_here
   FINANCIAL_API_KEY=your_key_here
   ```

3. **Run the Application**:
   ```bash
   streamlit run frontend/app.py
   ```
