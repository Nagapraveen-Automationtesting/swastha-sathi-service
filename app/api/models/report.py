from beanie import Document
from typing import List
from pydantic import BaseModel
from datetime import datetime



class ReportPayload(BaseModel):
    filePath: str

class Vital(BaseModel):
    param_name: str
    unit: str
    value: str
    normal_range: str

# Main MongoDB document model
class MedicalReport(Document):
    user_uid: str
    uploaded_at: datetime
    report_date: datetime
    report_number: str
    hospital_name: str
    vitals: List[Vital]
    raw_text: str
    tags: List[str]
    extracted_by: str
    created_at: datetime

    class Settings:
        collection = "DiagnosticReports"  # MongoDB collection name

