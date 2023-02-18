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
