from fastapi import APIRouter, Depends, Response, Header, status
from fastapi.responses import JSONResponse
from urllib3.exceptions import MaxRetryError, LocationValueError

import api.main
from api.inspection.technology.response import APIResponse
from api.inspection.inspection import Inspection, InvalidWebsiteException
from api.models.database import SessionLocal
from api.models.requestcache import RequestCacheService
from api.models.requests import RequestsService
from api.schemas import infoSchema, inspectionSchema, invalidRequestSchema

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
	reply     = APIResponse()
	reply.url = site_url

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
