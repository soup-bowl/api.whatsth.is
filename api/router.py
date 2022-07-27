import re, redis, json, yaml, urllib3
from typing import Optional
from fastapi import APIRouter, Depends, Response, Header, status, Request
from fastapi.responses import JSONResponse
from os import getenv
from urllib.parse import unquote
from urllib3.exceptions import MaxRetryError, LocationValueError
from dns.rdatatype import UnknownRdatatype
from dns.resolver import NXDOMAIN

from api import main
from api.inspection.technology.response import APIResponse
from api.inspection.inspection import Inspection, InvalidWebsiteException
from api.dnslookup import DNSLookup
from api.schemas import infoSchema, inspectionSchema, dnsProbeSchema, dnsAcceptedSchema, invalidRequestSchema

router = APIRouter()

@router.get("/", response_model=invalidRequestSchema)
async def root():
	return {
		"success": False,
		"message": "No URL specified"
	}

@router.get("/info", response_model=infoSchema)
async def information(request: Request):
	"""Returns some rudimentary server information.
	"""
	print()
	return {
		"success": True,
		"api_version": request.app.version,
	}

@router.get("/inspect/{site_url:path}", tags=["inspection"], response_model=inspectionSchema, responses={400: {"model": invalidRequestSchema}})
async def inspect_site(site_url: str, response: Response, req_ip: str = Header(None, alias='X-Real-IP')) -> dict:
	"""The specified URL will be in-turn called by the system. The system will then perform various inspections on the
	response data and the connection to calculate what technology the website is running. In certain conditions, if the
	site is detected to be using a known REST API, useful data will also be harvested from their endpoint.

	This is request-intensive, and results in a slow repsonse currently. To counter this, a caching engine is used to
	serve repeat requests with the same data.
	"""

	# Check for inspection instructions, and reloads them if they've expired.
	defs = None
	has_defs = await main.app.state.rcache.get_value('InspectionDefs')
	if has_defs is None:
		def_url = getenv('WTAPI_DEFINITION_URL', 'https://gist.githubusercontent.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1/raw/definitions.yml')
		def_file = urllib3.PoolManager().request('GET', def_url)
		if def_file.status == 200:
			print("Loaded latest definition file from GitHub.")
			resp = def_file.data.decode('utf-8')
			defs = yaml.safe_load(resp)
			await main.app.state.rcache.set_value('InspectionDefs', resp, 2629800)
		else:
			print("Unable to download definitions file.")
	else:
		defs = yaml.safe_load(has_defs)
	
	site_url = unquote(site_url)

	# Check for an existing cached version and return that.
	cache_contents = await main.app.state.rcache.get_value('InspectionCache-' + site_url)
	if cache_contents is not None:
		return json.loads(cache_contents)
	else:
		reply = APIResponse()
		reply.url = site_url if bool(re.search('^https?://.*', site_url)) else 'https://' + site_url

		try:
			inspector = Inspection(url=reply.url, config=defs)
			reply.success = True
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

		if reply.success == True:
			cache_contents = await main.app.state.rcache.set_value('InspectionCache-' + site_url, json.dumps(reply.asdict()), 86400)
			return reply.asdict()
		

		return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=reply.asdict())

@router.get("/dns/{protocol}/{site_url:path}", tags=["dns"], response_model=dnsProbeSchema, responses={400: {"model": invalidRequestSchema}})
async def dns_prober(protocol: str, site_url: str, response: Response) -> dict:
	"""This endpoint will run a DNS check on the specified URL, and return the information collected from the lookup.
	"""

	cache_contents = await main.app.state.rcache.get_value('DnsCache-' + site_url)
	if cache_contents is not None:
		return json.loads(cache_contents)
	else:
		success = True
		message = ''

		try:
			probelook = DNSLookup().probe(protocol, site_url)
		except UnknownRdatatype as e:
			success = False
			message = "The specified RR '%s' is either unsupported or does not exist." % protocol
		except NXDOMAIN as e:
			success = False
			message = "The requested URL does not exist."

		if success == False:
			return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"success": False, "message": message})

		if probelook.success == True:
			cache_contents = await main.app.state.rcache.set_value('DnsCache-' + site_url, json.dumps(probelook.asdict()))
			return probelook.asdict()

@router.get("/dns/protocols", tags=["dns"], response_model=dnsAcceptedSchema)
async def dns_probe_option() -> dict:
	"""Returns a list of supported protocol types that the API will accept.
	"""
	return {
		'records': [
			{ 'type': 'A', 'name': 'Address (IPv4)' },
			{ 'type': 'AAAA', 'name': 'Address (IPv6)' },
			{ 'type': 'CNAME', 'name': 'Canonical Name' },
			{ 'type': 'MX', 'name': 'Mail Exchange' },
			{ 'type': 'NS', 'name': 'Name Server' },
			{ 'type': 'TXT', 'name': 'Text' }
		]
	}
