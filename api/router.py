import re
from fastapi import APIRouter, Depends, Response, Header, status
from fastapi.responses import JSONResponse
from urllib.parse import unquote
from urllib3.exceptions import MaxRetryError, LocationValueError
from dns.rdatatype import UnknownRdatatype

import api.main
from api.inspection.technology.response import APIResponse
from api.inspection.inspection import Inspection, InvalidWebsiteException
from api.dnslookup import DNSLookup
from api.models.database import SessionLocal
from api.models.requestcache import RequestCacheService
from api.models.requests import RequestsService
from api.schemas import infoSchema, inspectionSchema, dnsProbeSchema, dnsAcceptedSchema, invalidRequestSchema

router = APIRouter()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@router.get("/", response_model=invalidRequestSchema)
async def root():
	return {
		"success": False,
		"message": "No URL specified"
	}

@router.get("/info", response_model=infoSchema)
async def information(db: SessionLocal = Depends(get_db)):
	"""Returns some rudimentary, anonymous usage data that the tool has collected for general interest.
	"""
	return {
		"success": True,
		"counts": RequestsService(db).getRequestFrequency(),
	}

@router.get("/inspect/{site_url:path}", tags=["inspection"], response_model=inspectionSchema, responses={400: {"model": invalidRequestSchema}})
async def inspect_site(site_url: str, response: Response, req_ip: str = Header(None, alias='X-Real-IP'), db: SessionLocal = Depends(get_db)) -> dict:
	"""The specified URL will be in-turn called by the system. The system will then perform various inspections on the
	response data and the connection to calculate what technology the website is running. In certain conditions, if the
	site is detected to be using a known REST API, useful data will also be harvested from their endpoint.

	This is request-intensive, and results in a slow repsonse currently. To counter this, a caching engine is used to
	serve repeat requests with the same data.
	"""
	site_url = unquote(site_url)

	reply     = APIResponse()
	reply.url = site_url if bool(re.search('^https?://.*', site_url)) else 'https://' + site_url

	try:
		inspector        = Inspection(url=reply.url, cache=RequestCacheService(db), config=api.main.config)
		reply.success    = True
		reply.inspection = inspector.get_site_details().asdict()
	except InvalidWebsiteException as e:
		reply.success = False
		reply.message = str(e)
	except MaxRetryError as e:
		reply.success = False
		reply.message = 'Invalid URL or permission denied'
	except LocationValueError as e:
		reply.success = False
		reply.message = 'No URL specified'
	
	RequestsService(db).setInfo(reply.url)

	if reply.success == True:
		return reply.asdict()

	return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=reply.asdict())

@router.get("/dns/{protocol}/{site_url:path}", tags=["dns"], response_model=dnsProbeSchema, responses={400: {"model": invalidRequestSchema}})
async def dns_prober(protocol: str, site_url: str, response: Response) -> dict:
	"""This endpoint will run a DNS check on the specified URL, and return the information collected from the lookup.
	"""
	success = True
	message = ''

	try:
		probelook = DNSLookup().probe(protocol, site_url)
	except UnknownRdatatype as e:
		success = False
		message = "The specified RR '%s' is either unsupported or does not exist." % protocol

	if success == False:
		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})

	if probelook.success == True:
		return probelook.asdict()

@router.get("/dns/protocols", tags=["dns"], response_model=dnsAcceptedSchema)
async def dns_probe_option() -> dict:
	"""Returns a list of supported protocol types that the API will accept.
	"""
	return {
		'records': [
			'A',
			'CNAME',
			'MX'
		]
	}
