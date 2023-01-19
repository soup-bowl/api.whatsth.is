"""aaaaaaaaaaaaaaaaaaa
"""

import urllib3
from lxml import html

class BaseInspection():
	def __init__(self):
		self.pool_manager = urllib3.PoolManager()
		# We set a browser-matched user agent as some sites use simple UA match to block the request.
		self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0"
		self.headers = None
		self.parsed = None
	
	def parse_input_url(self, url: str):
		"""Sets the object with the XML information taken from the input URL.

		Args:
			url (str): The URL to retrieve.
		
		Raises:
			InvalidWebsiteException: The given URL has caused a problem, typically either non-existent or access denied.
		"""
		request = self.pool_manager.request('GET', url, headers={'User-Agent': self.user_agent})

		if request.status != 200:
			raise InvalidWebsiteException(str(request.status) + " - Site did not respond with a successful connection.")

		self.headers = request.headers
		self.parsed = html.fromstring(request.data)
