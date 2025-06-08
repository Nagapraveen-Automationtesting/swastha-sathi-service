import os
import traceback
from datetime import datetime
from typing import Type, TypeVar

import requests
from fastapi import UploadFile, File

from app.api.core.db import BaseRepository

T = TypeVar("T")
# Define the endpoint and file path

# file_path = 'D:/Praveen/Library/OCR/SampleData/1206CHOWSEN.pdf'

# Open the file in binary mode
# with open(file_path, 'rb') as f:
#     files = {'report': f}
#     response = requests.post(url, files=files)
#
# # Print the response
# print("Status Code:", response.status_code)
# print("Response JSON:", response.json())
class InHouseOCR:
    def __init__(self):
        pass

    def extract_vitals_from_in_house_model(self, file_path: str):
        try:
            url = 'http://127.0.0.1:8003/upload-report'

            with open(file_path, 'rb') as f:
                files = {
                    'report': (os.path.basename(file_path), f, 'application/octet-stream')
                }
                print(f"Calling OCR service with file: {file_path}")
                response = requests.post(url, files=files)
                return response.json()
        except Exception as e:
            print("Error in OCR call:", e)
            return {"error": str(e)}

    def extract_vitals_from_ss_ocr(self, file_path: str):
        try:
            url = 'http://127.0.0.1:8002/extract-vitals'

            response = requests.post(url, params = {"path" : file_path})
            return response.json()
        except Exception as e:
            print("Error in OCR call:", e)
            return {"error": str(e)}

    from pymongo import MongoClient
    from datetime import datetime

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017")  # Update with your MongoDB URI
    db = client["medical_reports"]  # Your database name
    collection = db["reports"]  # Your collection name

    # Function to update MongoDB document
    async def update_report(model: Type[T], report_number: str, extracted_vitals: dict):
        # Prepare update data
        update_fields = {
            "hospital_name": extracted_vitals.get("Hospital Name", ""),
            "report_date": datetime.strptime(extracted_vitals.get("Report Date", ""),
                                             "%d-%b-%y").isoformat() if extracted_vitals.get("Report Date") else None,
            "report_number": extracted_vitals.get("Report Number", ""),
            "vitals": [
                {
                    "param_name": vital["Param Name"],
                    "unit": vital["Unit"],
                    "value": vital["Value"],
                    "normal_range": vital["Normal Range"]
                } for vital in extracted_vitals.get("Vitals", [])
            ]
        }

        # Insert or update the document
        await BaseRepository.insert_one(model, update_fields)


ss_ocr_new = InHouseOCR()