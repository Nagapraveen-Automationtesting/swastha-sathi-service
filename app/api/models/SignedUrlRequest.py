
from pydantic import BaseModel

class SignedUrlRequest(BaseModel):
    fileName: str
    fileType: str