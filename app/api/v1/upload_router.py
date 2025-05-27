import traceback

from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from app.api.services.mistral_ocr import mistral_ocr
from app.api.services.ss_ocr_new import ss_ocr_new
import shutil
import os
import uuid


upload_router = APIRouter()

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
