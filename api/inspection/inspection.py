"""Inspection API interaction library.
"""

from typing import Any
import urllib3
from lxml import html

from api.inspection.technology.wordpress import WordPressIdentifier

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
		"""Name property.

		Returns:
			[str]: Returns the name.
		"""
		return self._name

	@property
	def technology(self) -> str:
		"""Technology property.

		Returns:
			[str]: Returns the technology.
		"""
		return self._technology

	@property
	def matched_on(self) -> list:
		"""Matched property.

		Returns:
			[list]: Returns the matches.
		"""
		return self._matched_on

	@property
	def match_count(self) -> int:
		"""Match count property.

		Returns:
			[int]: Returns the matches count.
		"""
		return self._match_count

	@property
	def match_total(self) -> int:
		"""Match total property.

		Returns:
			[int]: Returns the match total.
		"""
		return self._match_total

	@property
	def additional(self) -> Any:
		"""Additional property.

		Returns:
			[Any]: Returns the additions if they exist.
		"""
		return self._additional

	@name.setter
	def name(self, name: str) -> None:
		"""Name property.

		Args:
			name (str): Sets the name.
		"""
		self._name = name

	@technology.setter
	def technology(self, technology: str) -> None:
		"""Technology property.

		Args:
			technology (str): Sets the technology.
		"""
		self._technology = technology

	@matched_on.setter
	def matched_on(self, matched_on: list) -> None:
		"""Matched property.

		Args:
			matched_on (list): Sets the matches.
		"""
		self._matched_on = matched_on

	@match_count.setter
	def match_count(self, count: int) -> None:
		"""Match count property.

		Args:
			count (int): Sets the match count.
		"""
		self._match_count = count

	@match_total.setter
	def match_total(self, count: int) -> None:
		"""Match total property.

		Args:
			count (int): Sets the match total.
		"""
		self._match_total = count

	@additional.setter
	def additional(self, additional) -> None:
		"""Additional property.

		Args:
			additional (Any): Sets the additionals.
		"""
		self._additional = additional

	def add_match(self, match_string) -> None:
		"""Adds a match to the collection and the count.

		Args:
			match_string (Any): Inputs the match string.
		"""
		self._matched_on.append(match_string)
		self._match_count = self._match_count + 1

	def asdict(self) -> dict:
		"""Converts the Python object into a generic dictionary.

		Returns:
			[dict]: Generic dictionary representation.
		"""
		return {
			'name': self.name,
			'technology': self.technology,
			'matched_on': self.matched_on,
			'additional': self.additional.asdict() if self.additional is not None else None,
		}

class Inspection():
	"""Inspection interactions handler.
	"""
	def __init__(self, url: str, config: dict):
		self.reply = InspectionResult()
		self.config = config
		self.pool_manager = urllib3.PoolManager()
		self.url = url
		self.headers = None
		self.parsed = None
		# We set a browser-matched user agent as some sites use simple UA match to block the request.
		self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0"

	def get_site_details(self) -> InspectionResult:
		"""Gets top-level website information by scraping the specified site HTML.

		Raises:
			InvalidWebsiteException: The given URL has caused a problem, typically either non-existent or access denied.

		Returns:
			InspectionResult: Detection results.
		"""

		request = self.pool_manager.request('GET', self.url, headers={'User-Agent': self.user_agent})

		if request.status != 200:
			raise InvalidWebsiteException(str(request.status) + " - Site did not respond with a successful connection.")

		self.headers = request.headers
		self.parsed = html.fromstring(request.data)

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
