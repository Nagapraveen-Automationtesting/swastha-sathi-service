import traceback
from datetime import timedelta

from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from fastapi.responses import JSONResponse

from app.api.models.SignedUrlRequest import SignedUrlRequest
from app.api.services.mistral_ocr import mistral_ocr
from app.api.services.ss_ocr_new import ss_ocr_new
from google.cloud import storage
import shutil
import os
import uuid

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("./GCP/swasthasathi-287428f89337.json")

upload_router = APIRouter()

BUCKET_NAME = "ss-ocr"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@upload_router.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):
    try:
        # Save uploaded file locally
        file_ext = file.filename.split('.')[-1]
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{file_ext}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call MistralOCR
        result = ss_ocr_new.extract_vitals_from_in_house_model(file_path)
        print(f"Extracted Vitals: {result}")
        return JSONResponse(content=result)

    except Exception as e:
        # traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@upload_router.post("/get-signed-url")
def get_signed_url(request_data: SignedUrlRequest):
    try:
        print(f"Came here with request data: {request_data}")
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(request_data.fileName)

        # Set expiration time for the signed URL
        expiration = timedelta(minutes=10)
        print(f"Before reaching ")
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="PUT",
            content_type=request_data.fileType,
        )
        print(f"After reaching bubket")

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{request_data.fileName}"
        print(f"Generated signed URL: {signed_url}, Public URL: {public_url}")
        return {
            "signedUrl": signed_url,
            "publicUrl": public_url,
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating signed URL: {str(e)}")
