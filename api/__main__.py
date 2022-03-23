import os, tempfile, urllib3, falcon
from wsgiref.simple_server import make_server

from api.config import Config
from api.server import Server

hostname = "0.0.0.0"
port     = 43594

if __name__ == "__main__":
	def_url  = 'https://gist.githubusercontent.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1/raw/definition.json'
	def_file = urllib3.PoolManager().request('GET', def_url)

	config = Config()

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

	app = falcon.App()
	app.add_sink(Server(config=config).on_get, prefix='/')

	try:
		with tempfile.TemporaryDirectory() as td:
			with make_server(host=hostname, port=port, app=app) as httpd:
				config.tmpdir = td
				print("Cache dir: " + config.tmpdir)
				print("----")
				httpd.serve_forever()
	except KeyboardInterrupt:
		pass
