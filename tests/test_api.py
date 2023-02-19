"""tests
"""

import yaml
import unittest
import urllib3
from api.inspection.inspection import Inspection

class StatChecks(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		"""Temp.
		"""
		def_file = urllib3.PoolManager().request(
			'GET',
			'https://gist.githubusercontent.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1/raw/definitions.yml'
		).data.decode('utf-8')
		self.config = yaml.safe_load(def_file)

	def test_generic_detections(self):
		"""Checks the definitions of the checks.
		"""

		# WordPress
		inspector = Inspection(url='https://wordpress.org/', config=self.config).get_site_details()
		self.assertEqual(inspector['technology']['cms']['name'], 'WordPress')
		# Unknown, but exists.
		inspector = Inspection(url='https://example.com/', config=self.config).get_site_details()
		self.assertEqual(inspector['technology']['cms'], None)

