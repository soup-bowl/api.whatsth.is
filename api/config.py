from sys import argv
from os.path import realpath, exists
from pathlib import Path
import json, os, getopt

class Config(object):
	def __init__(self):
		self.path    = None
		self.content = None
		self.loaded  = False
	
	def load(self, path):
		if exists( path ):
			self.path    = path
			self.content = json.loads( Path( path ).read_text() )
			self.loaded  = True

			return True
		else:
			return False

	def has_config(self):
		return self.loaded
	
	def get(self):
		return self.content
