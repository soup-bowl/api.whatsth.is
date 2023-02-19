"""Inspection API interaction library.
"""

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
				'cdn': self.identify_technology('cdn', match_all=True),
			},
			'additional': None
		}

	def identify_technology(self, technology: str, match_all: bool = False):
		"""Runs a header check & XPath scraping routine to the in-memory XML using the loaded-in detection config.
		"""

		collection = []

		checkpoints = self.config[technology]
		for checkpoint in checkpoints:
			datacoll = {
				'name': None,
				'description': None,
				'url': None,
				'match_available': 0,
				'match_on': []
			}

			if 'headers' in checkpoints[checkpoint]:
				for check in checkpoints[checkpoint]['headers']:
					key,value = check.split(':', 1)
					if key in self.headers:
						if self.headers[key] == value.strip():
							datacoll['match_on'].append(check)
			if 'body' in checkpoints[checkpoint]:
				for check in checkpoints[checkpoint]['body']:
					hits = self.parsed.xpath(check)
					if len(hits) > 0:
						datacoll['match_on'].append(check)

			if len(datacoll['match_on']) > 0:
				datacoll['name'] = checkpoints[checkpoint]['name']
				datacoll['description'] = checkpoints[checkpoint]['description']
				datacoll['url'] = checkpoints[checkpoint]['url']
				datacoll['match_available'] = (
					len(checkpoints[checkpoint]['body']) if 'body' in checkpoints[checkpoint] else 0 +
					len(checkpoints[checkpoint]['headers']) if 'headers' in checkpoints[checkpoint] else 0
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
