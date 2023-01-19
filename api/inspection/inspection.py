"""Inspection API interaction library.
"""

from typing import Any
import urllib3
from lxml import html

from api.inspection.technology.wordpress import WordPressIdentifier
from api.inspection.base import BaseInspection

class InspectionResult():
	"""Inspection result collection object.
	"""
	def __init__(self):
		self._name = ''
		self._technology = 'Unknown'
		self._matched_on = []
		self._match_count = 0
		self._match_total = 0
		self._additional = None

	@property
	def name(self) -> str:
		return self._name

	@property
	def technology(self) -> str:
		return self._technology

	@property
	def matched_on(self) -> list:
		return self._matched_on

	@property
	def match_count(self) -> int:
		return self._match_count

	@property
	def match_total(self) -> int:
		return self._match_total

	@property
	def additional(self) -> Any:
		return self._additional

	@name.setter
	def name(self, name: str) -> None:
		self._name = name

	@technology.setter
	def technology(self, technology: str) -> None:
		self._technology = technology

	@matched_on.setter
	def matched_on(self, matched_on: list) -> None:
		self._matched_on = matched_on

	@match_count.setter
	def match_count(self, count: int) -> None:
		self._match_count = count

	@match_total.setter
	def match_total(self, count: int) -> None:
		self._match_total = count

	@additional.setter
	def additional(self, additional) -> None:
		self._additional = additional

	def add_match(self, match_string) -> None:
		self._matched_on.append(match_string)
		self._match_count = self._match_count + 1

	def asdict(self) -> dict:
		return {
			'name': self.name,
			'technology': self.technology,
			'matched_on': self.matched_on,
			'additional': self.additional.asdict() if self.additional is not None else None,
		}

class Inspection(BaseInspection):
	"""Inspection interactions handler.
	"""
	def __init__(self, url: str, config: dict):
		super(Inspection, self).__init__()
		self.reply = InspectionResult()
		self.config = config
		self.url = url
		

	def get_site_details(self) -> InspectionResult:
		"""Gets top-level website information by scraping the specified site HTML.

		Raises:
			InvalidWebsiteException: The given URL has caused a problem, typically either non-existent or access denied.

		Returns:
			InspectionResult: Detection results.
		"""

		self.parse_input_url(self.url)

		self.get_title()
		self.identify_cms()

		if self.reply.technology == 'WordPress':
			try:
				wp_api_url = self.parsed.xpath('/html/head/link[@rel="https://api.w.org/"]')[0].attrib['href']
				self.reply.additional = WordPressIdentifier(wp_api_url).get()
			except IndexError:
				attempt = self.pool_manager.request('GET', self.url + '/wp-json')
				if attempt.status == 200:
					self.reply.additional = WordPressIdentifier(self.url + '/wp-json').get()
				else:
					pass

		return self.reply

	def get_title(self) -> None:
		"""Sets the page title.
		"""

		self.reply.name = self.parsed.xpath('/html/head/title')[0].text

	def identify_cms(self) -> None:
		"""Runs a header check & XPath scraping routine to the in-memory XML using the loaded-in detection config.
		"""

		checkpoints = self.config['cms']
		for cms in checkpoints:
			if 'headers' in checkpoints[cms]:
				for check in checkpoints[cms]['headers']:
					key,value = check.split(':', 1)
					if key in self.headers:
						if self.headers[key] == value.strip():
							self.reply.add_match(check)
			if 'body' in checkpoints[cms]:
				for check in checkpoints[cms]['body']:
					hits = self.parsed.xpath(check)
					if len(hits) > 0:
						self.reply.add_match(check)

			if self.reply.match_count > 0:
				self.reply.match_total = (
					len(checkpoints[cms]['body']) if 'body' in checkpoints[cms] else 0 +
					len(checkpoints[cms]['headers']) if 'headers' in checkpoints[cms] else 0
				)
				self.reply.technology = self.nicename(cms)
				return

	def nicename(self, identifier: str) -> str:
		"""Returns the proper product identifier based on the detection ID.

		Args:
			identifier (str): The product ID/key from the configuration file.

		Returns:
			str: The correctly-styled CMS name, or a first letter capitalisation if non-existent.
		"""

		if identifier == "wordpress":
			return "WordPress"
		if identifier == "joomla":
			return "Joomla!"
		if identifier == "shopify":
			return "Shopify"
		if identifier == "phpbb":
			return "PHPBB"

		return identifier.capitalize()

class InvalidWebsiteException(Exception):
	"""Invalid website exception.
	"""
