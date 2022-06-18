from typing import Optional, List
from pydantic import BaseModel

class DetectionSchema(BaseModel):
	name: str
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
	url: Optional[str]

class InfoCountSchema(BaseModel):
	week: int
	month: int
	quarter: int
	year: int

class infoSchema(BaseModel):
	success: bool = True
	counts: InfoCountSchema

class dnsProbeRecordSchema(BaseModel):
	address: Optional[str]
	priority: Optional[int]
	text: Optional[tuple]

class dnsProbeSchema(BaseModel):
	success: bool = True
	url: str
	type: str
	records: List[dnsProbeRecordSchema]

class dnsAcceptedItemsSchema(BaseModel):
	type: str
	name: str

class dnsAcceptedSchema(BaseModel):
	success: bool = True
	records: List[dnsAcceptedItemsSchema]
