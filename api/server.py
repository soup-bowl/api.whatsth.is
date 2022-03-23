import json, os, tempfile, urllib3, falcon
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib3.exceptions import MaxRetryError, LocationValueError

from api.apiresponse import APIResponse
from api.inspection import Inspection, InvalidWebsiteException
from api.config import Config

class Server:
	def __init__(self, config):
		self.config = config

	"""Run a continuously serving HTTP server.
	"""
	def on_get(self, request, response):
		"""Handles incoming GET requests to the server.
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

