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
                    extracted_tables.append({"table_data": cleaned_table})
                    
        return ParsedDocument(
            source_file=file_path,
            file_type="pdf",
            text_content=full_text.strip(),
            tables=extracted_tables
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
                
        return ParsedDocument(
            source_file=file_path,
            file_type="spreadsheet",
            text_content="Spreadsheet parsed. See tables array for structured data.",
            tables=tables
        )

# Simple test block
if __name__ == "__main__":
    agent = IngestionAgent()
    print("Ingestion Agent loaded and ready.")
