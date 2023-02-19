"""Schema collection.
"""

from typing import Optional, List
from pydantic import BaseModel

class DetectionTechnologyResponseSchema(BaseModel):
	"""Responses from the tech inspection.
	"""

	name: str
	description: str
	url: str
	match_available: int
	match_on: List[str]

class DetectionTechnologySchema(BaseModel):
	"""Inspection technology list.
	"""

	cms: Optional[DetectionTechnologyResponseSchema]
	frontend: Optional[DetectionTechnologyResponseSchema]
	javascript: List[DetectionTechnologyResponseSchema]
	cdn: List[DetectionTechnologyResponseSchema]


class DetectionSchema(BaseModel):
	"""Detection response schema.
	"""

	title: Optional[str]
	technology: DetectionTechnologySchema
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

class DNSProbeAllRecordsMXSchema(BaseModel):
	address: str
	priority: int

class DNSProbeAllRecordsSchema(BaseModel):
	A: List[str]
	AAAA: List[str]
	CNAME: List[str]
	MX: List[DNSProbeAllRecordsMXSchema]
	TXT: List[str]
	NS: List[str]

class DNSProbeAllSchema(BaseModel):
	"""DNS API schema for all record types.
	"""

	success: bool = True
	message: Optional[str]
	records: DNSProbeAllRecordsSchema

class WhoisSchema(BaseModel):
	"""whois lookup schema.
	"""

	success: bool = True
	domain: str = "EXAMPLE.DOMAIN"
	registrar: str = "Contoso Ltd."
	whois_operator: Optional[str] = "whois.example.lookup"
	nameservers: List[str] = ["ns1.example.lookup", "ns2.example.lookup", "ns3.example.lookup"]
	date_created: str = "1998-02-12T10:11:12"
	date_updated: str = "2022-02-12T10:11:12"
	date_expires: str = "2033-02-12T10:11:12"
