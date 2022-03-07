from api.inspection import Inspection, InvalidWebsiteException
from api.config import Config

import unittest, os

class StatChecks(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.config = Config()
		self.config.load('detection.json')

	def test_generic_detections(self):
		"""Checks the operationality of the checks.
		"""
		# WordPress
		inspector = Inspection(self.config, 'https://wordpress.org/').get_site_details()
		self.assertEqual(inspector['technology'], 'WordPress')
		# Unknown, but exists.
		inspector = Inspection(self.config, 'https://example.com/').get_site_details()
		self.assertEqual(inspector['technology'], 'Unknown')

	def test_nicename(self):
		"""Check the nice name generator uses the in-built values, and capitalises unknown ones.
		"""
		inspector = Inspection(self.config, 'dummy')
		self.assertEqual(inspector.nicename('wordpress'), 'WordPress')
		self.assertEqual(inspector.nicename('madeupcms'), 'Madeupcms')
