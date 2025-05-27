import traceback

import requests
from fastapi import UploadFile, File

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

    def extract_vitals_from_in_house_model(self, report: UploadFile = File(...)):
        try:
            """
            This function simulates the extraction of vitals from a text using an in-house model.
            For demonstration purposes, it returns a hardcoded JSON structure.
            """
            url = 'http://0.0.0.0:8003/upload-report'
            # Simulated response from an in-house model
            files = {
                # 'report': (file.filename, file.file, file.content_type)
            }

            response = requests.post(url, files=report)
            return response
        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}

ss_ocr_new = InHouseOCR()