import unittest, json
from api.inspection.inspection import Inspection

class StatChecks(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.config = json.loads('{"cms":{"wordpress":{"body":["/html/head/link[@href=\'//s.w.org\']"]}}}')

	def test_generic_detections(self):
		"""Checks the definitions of the checks.
		"""

		# WordPress
		inspector = Inspection(url='https://wordpress.org/', config=self.config).get_site_details()
		self.assertEqual(inspector.technology, 'WordPress')
		# Unknown, but exists.
		inspector = Inspection(url='https://example.com/', config=self.config).get_site_details()
		self.assertEqual(inspector.technology, 'Unknown')

	def test_nicename(self):
		"""Check the nice name generator uses the in-built values, and capitalises unknown ones.
		"""
		inspector = Inspection(url='dummy', config=self.config)
		self.assertEqual(inspector.nicename('wordpress'), 'WordPress')
		self.assertEqual(inspector.nicename('madeupcms'), 'Madeupcms')
