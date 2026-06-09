from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class ParsedDocument(BaseModel):
    """
    Schema for the output of the Ingestion Agent.
    Contains the raw and semi-structured data extracted from files.
    """
    source_file: str
    file_type: str
    text_content: str = ""
    tables: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}

class FinancialMetrics(BaseModel):
    """
    Schema for the output of the Analysis Agent.
    Contains strictly computed financial ratios and mathematically verified trends
    to avoid LLM hallucination.
    """
    ratios: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    trends: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    anomalies: List[str] = Field(default_factory=list)

class MarketIntelligence(BaseModel):
    """
    Schema for the output of the Market Intelligence Agent.
    Contains competitor multiples and sector benchmarks gathered via external APIs.
    """
    target_symbol: str
    target_metrics: Dict[str, Any] = Field(default_factory=dict)
    competitor_metrics: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    sector_benchmarks: Dict[str, float] = Field(default_factory=dict)
    market_context: str = ""

