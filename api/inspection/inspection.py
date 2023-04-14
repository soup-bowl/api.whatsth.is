"""Inspection API interaction library.
"""

import re
from typing import Any
import urllib3
from lxml import html

from api.inspection.technology.wordpress import WordPressIdentifier
from api.inspection.base import BaseInspection

class Inspection(BaseInspection):
	"""Inspection interactions handler.
	"""
	def __init__(self, url: str, config: dict):
		super(Inspection, self).__init__()
		self.config = config
		self.url = url


	def get_site_details(self) -> object:
		"""Gets top-level website information by scraping the specified site HTML.

		Raises:
			InvalidWebsiteException: The given URL has caused a problem, typically either non-existent or access denied.

		Returns:
			InspectionResult: Detection results.
		"""

		return {
			'title': self.parse_input_url(self.url),
			'technology': {
				'cms': self.identify_technology('cms'),
				'frontend': self.identify_technology('frontend'),
				'javascript': self.identify_technology('javascript', match_all=True),
				'seo': self.identify_technology('seo', match_all=True),
				'cdn': self.identify_technology('cdn', match_all=True),
				'language': self.identify_technology('language', match_all=True),
				'server': self.identify_technology('server', match_all=True),
			},
			'additional': None
		}

	def identify_technology(self, technology: str, match_all: bool = False):
		"""Runs a header check & XPath scraping routine to the in-memory XML using the loaded-in detection config.
		"""

		collection = []

		for checkpoint in self.config[technology]:
			datacoll = {
				'name': None,
				'description': None,
				'url': None,
				'match_available': 0,
				'match_on': []
			}

			if 'headers' in checkpoint:
				for check in checkpoint['headers']:
					key,value = check.split(':', 1)
					if key in self.headers:
						pattern = re.compile(value.strip(), re.IGNORECASE)
						match = pattern.search(self.headers[key])
						if match:
							datacoll['match_on'].append(check)

			if 'body' in checkpoint:
				for check in checkpoint['body']:
					hits = self.parsed.xpath(check)
					if hits is not False and len(hits) > 0:
						datacoll['match_on'].append(check)

			if len(datacoll['match_on']) > 0:
				datacoll['name'] = checkpoint['name']
				datacoll['description'] = checkpoint['description']
				datacoll['url'] = checkpoint['url']
				datacoll['match_available'] = (
					len(checkpoint['body']) if 'body' in checkpoint else 0 +
					len(checkpoint['headers']) if 'headers' in checkpoint else 0
				)

				if match_all is False:
					return datacoll
				else:
					collection.append(datacoll)

		if match_all:
			return collection
		else:
			return None

class InvalidWebsiteException(Exception):
	"""Invalid website exception.
	"""
