from fastapi import APIRouter, Response, status
from urllib3.exceptions import MaxRetryError, LocationValueError

import api.main
from api.inspection.technology.response import APIResponse
from api.inspection.inspection import Inspection, InvalidWebsiteException
from api.schemas import inspectionSchema, inspectionErrorSchema, invalidRequestSchema

router = APIRouter()

@router.get("/", response_model=invalidRequestSchema)
async def root():
    return {
        "success": False,
        "message": "No URL specified"
    }

@router.get("/inspect/{site_url:path}", tags=["inspection"], response_model=inspectionSchema, responses={400: {"model": inspectionErrorSchema}})
async def inspect_site(site_url: str, response: Response) -> dict:
    """The specified URL will be in-turn called by the system. The system will then perform various inspections on the
    response data and the connection to calculate what technology the website is running. In certain conditions, if the
    site is detected to be using a known REST API, useful data will also be harvested from their endpoint.

    This is request-intensive, and results in a slow repsonse currently. To counter this, a caching engine is used to
    serve repeat requests with the same data.

    Args:
        site_url (str): A URL-encoded string to a website to inspect.

    Returns:
        dict: Returns an API object.
    """
    reply     = APIResponse()
    reply.url = site_url

    try:
        inspector        = Inspection(reply.url, api.main.config, api.main.cache)
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

    if reply.success == True:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return reply.asdict()
