from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class FinancialEntity(BaseModel):
    label: str
    value: str
    confidence: float

class FinancialDocument(BaseModel):
    document_type: str
    institution: Optional[str] = None          # ← add = None
    customer_name: Optional[str] = None        # ← add = None
    account_number: Optional[str] = None       # ← add = None
    statement_period: Optional[str] = None     # ← add = None

    extracted_text: str
    entities: List[FinancialEntity] = Field(default_factory=list)  # safe default

    ingestion_date: date
    source_file: str