import os
from typing import Optional

from pydantic_settings import BaseSettings


from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SS_OCR_SERVICE_BASE_URL: Optional[str]
    SS_OCR_EXTRACT_VITALS_BASE_PATH: Optional[str]


settings = Settings()