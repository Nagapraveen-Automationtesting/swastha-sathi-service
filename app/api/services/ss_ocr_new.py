import os
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
ss_ocr_new = InHouseOCR()