from pydantic import BaseModel

class DetectionSchema(BaseModel):
    technology: str
    matched_on: list
    addditional: dict

class inspectionSchema(BaseModel):
    success: bool = True
    message: DetectionSchema
    url: str

class inspectionErrorSchema(BaseModel):
    success: bool = False
    message: str
    url: str

class invalidRequestSchema(BaseModel):
	success: bool = False
	message: str = "No URL specified"