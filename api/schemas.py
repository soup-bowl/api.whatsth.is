from typing import Optional
from pydantic import BaseModel

class DetectionSchema(BaseModel):
	technology: str
	matched_on: list
	additional: Optional[dict] = None

class inspectionSchema(BaseModel):
	success: bool = True
	message: DetectionSchema
	url: str

class invalidRequestSchema(BaseModel):
	success: bool = False
	message: str = "No URL specified"
	url: str
