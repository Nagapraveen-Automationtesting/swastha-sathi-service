import os

import requests

class MistralOCR:
    def __init__(self):
        # self.api_key = api_key
        self.api_url = "https://api.mistralocr.com/v1/parse"
        self.api_key = os.getenv("MISTRAL_API_KEY", "xozeGHoN2NlFpHNJ11Qy1NlzITbM7RXl")

    def extract_vitals(self, file_path: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        files = {
            "file": open(file_path, "rb")
        }

        try:
            response = requests.post(self.api_url, headers=headers, files=files)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error calling MistralOCR API: {e}")
            return {}

mistral_ocr = MistralOCR()