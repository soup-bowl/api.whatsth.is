import falcon

from urllib3.exceptions import MaxRetryError, LocationValueError

from api.apiresponse import APIResponse
from api.inspection import Inspection, InvalidWebsiteException

class Server:
	def __init__(self, config):
		self.config = config

	def on_get(self, request: falcon.Request, response: falcon.Response) -> None:
		"""Handles incoming GET requests to the server.

		Args:
			request (falcon.Request): Context coming in from the connection.
			response (falcon.Response): Object to populate with response criteria.
		"""

		reply     = APIResponse()
		reply.url = request.path[1:]

		try:
			inspector        = Inspection(self.config, reply.url)
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
			response.status = falcon.HTTP_200
		else:
			response.status = falcon.HTTP_400

		response.media = reply.asdict()
