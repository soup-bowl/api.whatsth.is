from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib3.exceptions import MaxRetryError
import json, os
from api.inspection import Inspection, InvalidWebsiteException

hostname = "0.0.0.0"
port     = 43594

class Server(BaseHTTPRequestHandler):
	"""Run a continuously serving HTTP server responding with system information and commands.
	"""
	def do_GET(self):
		"""Handles incoming GET requests to the server.
		"""

		try:
			inspector = Inspection(self.path[1:])
			site_details = inspector.get_site_details()
		except InvalidWebsiteException as e:
			self.fire_response(200, {
				'success': False,
				'message': str(e)
			})
			return
		except MaxRetryError as e:
			self.fire_response(200, {
				'success': False,
				'message': 'Unable to detect website'
			})
			return

		self.fire_response(200, {
			'success': True,
			'message': site_details
		})

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

	def fire_response(self, code, respo):
		"""Sends off the payload response down the HTTP channel.

		Args:
			code (int): HTTP response code, corresponding to https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
			respo (mixed): Dictionary or array to serve as the JSON response.
		"""
		self.set_headers(code, {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'})
		self.wfile.write(bytes(json.dumps(respo), "utf-8"))

if __name__ == "__main__":
	http_server = HTTPServer((hostname, port), Server)

	print(
		"What's this? Processor - Server started on %s (ctrl-c to close)." % ('http://' + hostname + ':' + str(port)),
		"source code: https://github.com/soup-bowl/api.whatsth.is",
		"----",
		sep=os.linesep
	)

	try:
		http_server.serve_forever()
	except KeyboardInterrupt:
		pass

	http_server.server_close()
	print(os.linesep + "Server stopped.")
