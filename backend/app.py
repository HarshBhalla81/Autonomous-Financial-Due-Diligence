import os
import sys
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Ensure the project's root is on the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.graph import DueDiligenceOrchestrator

app = FastAPI(
    title="Autonomous Financial Due Diligence API",
    version="1.0.0",
    description="A FastAPI wrapper around the LangGraph orchestrator that ingests a financial file, runs the AI agents, and returns the full due‑diligence state."
)

# Allow the Vercel‑deployed frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = DueDiligenceOrchestrator()

@app.post("/run_due_diligence")
async def run_due_diligence(
    target_symbol: str = Form(...),
    competitors: str = Form(...),  # comma‑separated list
    file: UploadFile = File(...)
):
    """Accept a file upload, target ticker, and competitor list, then execute the full LangGraph pipeline.
    Returns the entire state dictionary (including parsed document, financial metrics, market intel, risk assessment, and final memo).
    """
    # Save uploaded file to a temporary location inside the project
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, file.filename)
    try:
        with open(file_path, "wb") as out:
            content = await file.read()
            out.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store uploaded file: {e}")

    # Parse competitors string into a list, stripping whitespace and empty entries
    competitors_list = [c.strip() for c in competitors.split(",") if c.strip()]

    try:
        final_state = orchestrator.run_due_diligence(
            document_path=file_path,
            target_symbol=target_symbol,
            competitors=competitors_list,
        )
        return JSONResponse(content=final_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator error: {e}")
