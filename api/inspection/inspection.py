import urllib3, os
from lxml import html
from typing import Any, Optional
from api.config import Config

from api.inspection.technology.wordpress import WordPressIdentifier
from api.models.requestcache import RequestCacheService

class InspectionResult(object):
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
	def matched_on(self, matchedon: list) -> None:
		self._matched_on = matchedon

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

class Inspection(object):
	def __init__(self, url: str, config: Config, cache: Optional[RequestCacheService] = None):
		self.reply = InspectionResult()
		self.config = config
		self.cache = cache if os.getenv('WTAPI_NO_CACHE', '0') == '0' else None
		self.pm = urllib3.PoolManager()
		self.url = url
		self.headers = None
		self.parsed = None
		# We set a browser-matched user agent as some sites use simple UA match to block the request.
		self.ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0"

	def get_site_details(self) -> InspectionResult:
		"""Gets top-level website information by scraping the specified site HTML.

		Raises:
			InvalidWebsiteException: The given URL has caused a problem, typically either non-existent or access denied.

		Returns:
			InspectionResult: Detection results.
		"""

		if self.cache is not None:
			cacheReply = self.cache.getCachedInspection(self.url)
			if cacheReply is not None:
				return cacheReply

		request = self.pm.request('GET', self.url, headers={'User-Agent': self.ua})

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
				attempt = self.pm.request('GET', self.url + '/wp-json')
				if attempt.status == 200:
					self.reply.additional = WordPressIdentifier(self.url + '/wp-json').get()
				else:
					pass

		if self.cache is not None:
			self.cache.setCachedInspection(self.url, self.reply)

		return self.reply

	def get_title(self) -> None:
		"""Sets the page title.
		"""

		self.reply.name = self.parsed.xpath('/html/head/title')[0].text

	def identify_cms(self) -> None:
		"""Runs a header check & XPath scraping routine to the in-memory XML using the loaded-in detection config.
		"""

		checkpoints = self.config.get()['cms']
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
		elif identifier == "joomla":
			return "Joomla!"
		elif identifier == "shopify":
			return "Shopify"
		elif identifier == "phpbb":
			return "PHPBB"

		return identifier.capitalize()

class InvalidWebsiteException(Exception):
	pass
