"""Schema collection.
"""

from typing import Optional, List
from pydantic import BaseModel

class DetectionSchema(BaseModel):
	"""Detection response schema.
	"""

	name: str
	technology: str
	matched_on: list
	additional: Optional[dict] = None

class InspectionSchema(BaseModel):
	"""Inspection API response schema.
	"""

	success: bool = True
	message: DetectionSchema
	url: str

class InvalidRequestSchema(BaseModel):
	"""API error response schema.
	"""

	success: bool = False
	message: str = "No URL specified"
	url: Optional[str]

class InfoSchema(BaseModel):
	"""API information schema.
	"""

	success: bool = True
	api_version: str

class DNSProbeRecordSchema(BaseModel):
	"""Indvidual DNS response schema.
	"""

	address: Optional[str]
	priority: Optional[int]
	text: Optional[tuple]
	ttl: Optional[int]

class DNSProbeSchema(BaseModel):
	"""DNS API schema.
	"""

	success: bool = True
	url: str
	type: str
	records: List[DNSProbeRecordSchema]

class DNSAcceptedItemsSchema(BaseModel):
	"""DNS record type schema.
	"""

	type: str
	name: str

class DNSAcceptedSchema(BaseModel):
	"""DNS record type API schema.
	"""

	success: bool = True
	records: List[DNSAcceptedItemsSchema]
