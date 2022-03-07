import urllib3, unicodedata, re, json
from os import remove
from os.path import exists, getmtime
from pathlib import Path
from time import time
from lxml import html

class Inspection(object):
	def __init__(self, codes, url):
		self.codes   = codes
		self.pm      = urllib3.PoolManager()
		self.url     = url
		self.headers = None
		self.parsed  = None
		self.ua      = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0"

		self.cms         = "Unknown"
		self.match_count = 0
		self.match_total = 0
		self.matches     = []
		self.wp_api      = None

	def get_site_details(self):
		"""Gets top-level website information by scraping the specified site HTML.

		Raises:
			InvalidWebsiteException: The given URL has caused a problem, typically either non-existent or access denied.

		Returns:
			object: Detection results.
		"""

		if len(self.codes.tmpdir) != 0:
			cachename = self.codes.tmpdir + '/' + self.slugify(self.url) + '.json'
			if exists(cachename):
				print(time() - getmtime(cachename))
				if (time() - getmtime(cachename)) > 2629743:
					remove(cachename)
				else:
					print( "'%s' found in cache (%s left before expiry)." % (self.url, ( 2629743 - (time() - getmtime(cachename)) )) )
					return json.loads( Path( cachename ).read_text() )

		request = self.pm.request('GET', self.url, headers={'User-Agent': self.ua})

		if request.status != 200:
			raise InvalidWebsiteException(str(request.status) + " - Site did not respond with a successful connection.")

		self.headers = request.headers
		self.parsed  = html.fromstring(request.data)

		self.identifty_cms()

		try:
			self.wp_api = self.parsed.xpath('/html/head/link[@rel="https://api.w.org/"]')[0].attrib['href']
		except IndexError:
			pass

		reply = {
			'technology': self.cms,
			'matched_on': self.matches
		}

		if len(self.codes.tmpdir) != 0:
			pppp = self.codes.tmpdir + '/' + self.slugify(self.url) + '.json'
			with open(pppp, 'a') as f:
				f.write(json.dumps(reply, ensure_ascii=False))

		return reply

	def identifty_cms(self):
		"""Runs a header check & XPath scraping routine to the in-memory XML using the loaded-in detection config.
		"""

		checkpoints = self.codes.get()['cms']
		for cms in checkpoints:
			for check in checkpoints[cms]['headers']:
				key,value = check.split(':', 1)
				if key in self.headers:
					if self.headers[key] == value.strip():
						self.match_count = self.match_count + 1
						self.matches.append(check)
			for check in checkpoints[cms]['body']:
				hits = self.parsed.xpath(check)
				if len(hits) > 0:
					self.match_count = self.match_count + 1
					self.matches.append(check)

			if self.match_count > 0:
				self.match_total = len(checkpoints[cms]['body']) + len(checkpoints[cms]['headers'])
				self.cms         = self.nicename(cms)

				return

	def nicename(self, identifier):
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
		else:
			return identifier.capitalize()

	def slugify(self, value, allow_unicode=False):
		"""
		Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
		dashes to single dashes. Remove characters that aren't alphanumerics,
		underscores, or hyphens. Convert to lowercase. Also strip leading and
		trailing whitespace, dashes, and underscores.

		Code is from Django - https://github.com/django/django/blob/main/django/utils/text.py
		"""
		value = str(value)
		if allow_unicode:
			value = unicodedata.normalize("NFKC", value)
		else:
			value = (
				unicodedata.normalize("NFKD", value)
				.encode("ascii", "ignore")
				.decode("ascii")
			)
		value = re.sub(r"[^\w\s-]", "", value.lower())
		return re.sub(r"[-\s]+", "-", value).strip("-_")

class InvalidWebsiteException(Exception):
	pass
