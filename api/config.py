import json, yaml
from os.path import exists
from pathlib import Path

class Config(object):
	def __init__(self):
		self.path = None
		self.content = None
		self.loaded = False
		self.tmpdir = ""

	def load_file(self, path: str) -> bool:
		"""Load a detection json file into the system.

		Args:
			path (str): Filesystem location of the config json you wish to load in.

		Returns:
			bool: Success state of loading in the config.
		"""

		if exists( path ):
			self.path = path
			self.content = json.loads( Path( path ).read_text() )
			self.loaded = True

			return True
		return False

	def load_json(self, jsonfile:str) -> None:
		self.content = json.loads( jsonfile )
		self.loaded = True

	def load_yml(self, ymlfile:str) -> None:
		self.content = yaml.safe_load( ymlfile )
		self.loaded = True

	def has_config(self) -> bool:
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
