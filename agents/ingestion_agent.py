import os
import pandas as pd
import pdfplumber
import json
import sys

# Ensure core module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.schemas import ParsedDocument

class IngestionAgent:
    """
    The Ingestion Agent is responsible for parsing unstructured files (PDFs, Excel, CSV)
    and returning a normalized, structured JSON/Pydantic object.
    """
    
    def process_file(self, file_path: str) -> ParsedDocument:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at: {file_path}")
        
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            return self._parse_pdf(file_path)
        elif ext in ['.xlsx', '.xls', '.csv']:
            return self._parse_spreadsheet(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
            
    def _parse_pdf(self, file_path: str) -> ParsedDocument:
        print(f"Ingestion Agent: Extracting data from PDF -> {file_path}")
        full_text = ""
        extracted_tables = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Extract text
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
                
                # Extract tables
                tables = page.extract_tables()
                for table in tables:
                    # Clean up empty rows/cols in basic tables
                    cleaned_table = [[cell for cell in row if cell is not None] for row in table]
                    
                    # Convert to dictionary format similar to spreadsheet
                    if len(cleaned_table) > 1:
                        headers = cleaned_table[0]
                        dict_data = []
                        for row in cleaned_table[1:]:
                            row_dict = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
                            dict_data.append(row_dict)
                        extracted_tables.append({"sheet_name": f"Page_{page.page_number}", "data": dict_data})
                    
        # Apply Normalization
        normalized_tables = self._normalize_tables(extracted_tables)
                    
        return ParsedDocument(
            source_file=file_path,
            file_type="pdf",
            text_content=full_text.strip(),
            tables=normalized_tables
        )
        
    def _parse_spreadsheet(self, file_path: str) -> ParsedDocument:
        print(f"Ingestion Agent: Extracting data from Spreadsheet -> {file_path}")
        tables = []
        
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            tables.append({"sheet_name": "CSV", "data": df.to_dict(orient='records')})
        else:
            excel_data = pd.read_excel(file_path, sheet_name=None)
            for sheet_name, df in excel_data.items():
                tables.append({"sheet_name": sheet_name, "data": df.fillna("").to_dict(orient='records')})
                
        # Apply Normalization
        normalized_tables = self._normalize_tables(tables)
                
        return ParsedDocument(
            source_file=file_path,
            file_type="spreadsheet",
            text_content="Spreadsheet parsed. See tables array for structured data.",
            tables=normalized_tables
        )
        
    def _normalize_tables(self, tables: list) -> list:
        """
        Normalizes raw extracted tables into a standard internal taxonomy.
        This ensures the Analysis Agent always receives consistent keys like 'Revenue'.
        
        Note: In a full production setup, this function would pass the raw table to an 
        LLM (using LangChain) with a prompt like: "Map the following rows to our standard taxonomy."
        For speed and determinism, we use a robust semantic dictionary mapping here.
        """
        # Standard Taxonomy Mapping
        taxonomy_mapping = {
            "total sales": "Revenue",
            "net revenues": "Revenue",
            "top line": "Revenue",
            "sales": "Revenue",
            "cost of goods sold": "COGS",
            "cost of revenue": "COGS",
            "cost of sales": "COGS",
            "operating exp": "Operating Expenses",
            "total operating expenses": "Operating Expenses",
            "opex": "Operating Expenses",
            "net profit": "Net Income",
            "net earnings": "Net Income",
            "bottom line": "Net Income"
        }
        
        normalized_tables = []
        for table in tables:
            norm_table = {"sheet_name": table.get("sheet_name", "Unknown"), "data": []}
            
            for row in table.get("data", []):
                norm_row = {}
                for key, val in row.items():
                    # We assume the first column usually holds the metric name, or a column named "Metric"
                    if key.lower() in ["metric", "line item", "description", ""] or list(row.keys()).index(key) == 0:
                        raw_metric = str(val).strip().lower()
                        # Find the mapped standard metric, otherwise keep the original (capitalized)
                        mapped_metric = taxonomy_mapping.get(raw_metric, str(val).strip().title())
                        norm_row["Metric"] = mapped_metric
                    else:
                        norm_row[key] = val
                        
                norm_table["data"].append(norm_row)
            normalized_tables.append(norm_table)
            
        return normalized_tables

# Simple test block
if __name__ == "__main__":
    agent = IngestionAgent()
    print("Ingestion Agent loaded and ready.")
