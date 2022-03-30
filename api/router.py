from fastapi import APIRouter, Request, Response, status
from urllib3.exceptions import MaxRetryError, LocationValueError

import api.main
from api.inspection.technology.response import APIResponse
from api.inspection.inspection import Inspection, InvalidWebsiteException

router = APIRouter()

@router.get("/inspect/{site_url:path}", tags=["inspection"])
async def inspect_site(site_url: str, response: Response):
    reply     = APIResponse()
    reply.url = site_url

    try:
        inspector        = Inspection(api.main.config, reply.url)
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
