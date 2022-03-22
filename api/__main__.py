import json, os, tempfile, urllib3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib3.exceptions import MaxRetryError, LocationValueError

from api.apiresponse import APIResponse
from api.inspection import Inspection, InvalidWebsiteException
from api.config import Config

hostname = "0.0.0.0"
port     = 43594

config = Config()

class Server(BaseHTTPRequestHandler):
	"""Run a continuously serving HTTP server.
	"""
	def do_GET(self):
		"""Handles incoming GET requests to the server.
		"""

		reply     = APIResponse()
		reply.url = self.path[1:]

		try:
			inspector        = Inspection(config, self.path[1:])
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

		self.fire_response(reply)

	def set_headers(self, response_code, headers):
		"""Sets the response headers for the outgoing payload.

		Args:
			response_code (int): HTTP response code, corresponding to https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
			headers (dict): Dictionary of HTTP headers and their values.
		"""
		self.send_response(response_code)
		for key, value in headers.items():
			self.send_header(key, value)
		self.end_headers()

	def fire_response(self, response: APIResponse):
		"""Sends off the payload response down the HTTP channel.

		Args:
			response (APIResponse): Response object.
		"""
		code = 200 if response.success == True else 400
		cors = os.getenv('WT_CORS_POLICY', '*')
		self.set_headers(code, {'Content-type': 'application/json', 'Access-Control-Allow-Origin': cors})
		self.wfile.write(bytes(json.dumps(response.asdict()), "utf-8"))

if __name__ == "__main__":
	def_url  = 'https://gist.githubusercontent.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1/raw/definition.json'
	def_file = urllib3.PoolManager().request('GET', def_url)

	if def_file.status == 200:
		print("Loaded latest definition file from GitHub.")
		config.load_json( def_file.data.decode('utf-8') )
	else:
		print("Unable to download definitions file.")
		exit(1)

	print(
		"What's this? Processor - Server started on %s (ctrl-c to close)." % ('http://' + hostname + ':' + str(port)),
		"source code: https://github.com/soup-bowl/api.whatsth.is",
		"definitions: %s" % def_url,
		sep=os.linesep
	)

	http_server = HTTPServer((hostname, port), Server)

	try:
		with tempfile.TemporaryDirectory() as td:
			config.tmpdir = td
			print("Cache dir: " + config.tmpdir)
			print("----")
			http_server.serve_forever()
	except KeyboardInterrupt:
		pass

	http_server.server_close()
	print(os.linesep + "Server stopped.")
