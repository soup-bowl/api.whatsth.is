from sys import argv
from os.path import realpath, exists
from pathlib import Path
import json, os, getopt

class Config(object):
	def __init__(self):
		self.path    = None
		self.content = None
		self.loaded  = False
		self.tmpdir  = ""

	def load_file(self, path):
		"""Load a detection json file into the system.

		Args:
			path (str): Filesystem location of the config json you wish to load in.

		Returns:
			bool: Success state of loading in the config.
		"""

		if exists( path ):
			self.path    = path
			self.content = json.loads( Path( path ).read_text() )
			self.loaded  = True

			return True
		return False
	
	def load_json(self, jsonfile):
		self.content = json.loads( jsonfile )
		self.loaded  = True

	def has_config(self):
		"""Whether the class has a configuration loaded into memory.

		Returns:
			bool: State of the configuration.
		"""

		return self.loaded

	def get(self):
		"""Gets the data from the configuration file.

		Returns:
			object: Detection config.
		"""

		return self.content
