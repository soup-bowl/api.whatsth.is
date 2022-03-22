from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib3.exceptions import MaxRetryError, LocationValueError
import json, os, getopt, tempfile
from sys import argv
from os.path import realpath, exists
from pathlib import Path
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

		try:
			inspector = Inspection(config, self.path[1:])
			site_details = inspector.get_site_details()
		except InvalidWebsiteException as e:
			self.fire_response(200, {
				'success': False,
				'message': str(e),
				'url': self.path[1:]
			})
			return
		except MaxRetryError as e:
			self.fire_response(400, {
				'success': False,
				'message': 'Invalid URL or permission denied',
				'url': self.path[1:]
			})
			return
		except LocationValueError as e:
			self.fire_response(400, {
				'success': False,
				'message': 'No URL specified',
				'url': self.path[1:]
			})
			return

		self.fire_response(200, {
			'success': True,
			'message': site_details.asdict(),
			'url': self.path[1:]
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
		cors = os.getenv('WT_CORS_POLICY', '*')
		self.set_headers(code, {'Content-type': 'application/json', 'Access-Control-Allow-Origin': cors})
		self.wfile.write(bytes(json.dumps(respo), "utf-8"))

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(
			argv[1::],
			"f:",
			["file="]
		)
	except getopt.GetoptError:
		print("Invalid command.")
		exit(2)

	for opt, arg in opts:
			if opt in ("-f", "--file"):
				config.load( arg )

	if config.has_config() == False:
		if exists( 'detection.json' ):
			print("No config input specified. Loading local detection.json file.")
			config.load( realpath( 'detection.json') )

	if config.has_config() == False:
		print("No detection specification loaded (no argument or detection.json file available locally).")
		exit(3)

	print(
		"What's this? Processor - Server started on %s (ctrl-c to close)." % ('http://' + hostname + ':' + str(port)),
		"source code: https://github.com/soup-bowl/api.whatsth.is",
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
