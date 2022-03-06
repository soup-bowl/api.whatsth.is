import urllib3
from lxml import html

class Inspection(object):
	def __init__(self, url):
		self.pm      = urllib3.PoolManager()
		self.url     = url
		self.headers = None
		self.parsed  = None
		self.ua      = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0"

		self.cms         = "N/A"
		self.match_count = 0
		self.match_total = 0
		self.matches     = []
		self.wp_api      = None

	def get_site_details(self):
		request = self.pm.request('GET', self.url, headers={'User-Agent': self.ua})

		if request.status != 200:
			raise Exception(str(request.status) + " - Site did not respond with a successful connection.")

		self.headers = request.headers
		self.parsed  = html.fromstring( request.data )#.decode('utf-8') )

		self.identifty_cms()

		try:
			self.wp_api = self.parsed.xpath('/html/head/link[@rel="https://api.w.org/"]')[0].attrib['href']
		except IndexError:
			pass

		return {
			'technology': self.cms,
			'matched_on': self.matches
		}

	def identifty_cms(self):
		checkpoints = {
			'wordpress': {
				'headers': [
					'x-powered-by: WP Engine'
				],
				'body': [
					'/html/head/link[@rel="https://api.w.org/"]',
					'/html/head/link[@href="//s.w.org"]',
					'//*[@id="wp-custom-css"]'
				]
			},
			'shopify': {
				'headers': [],
				'body': [
					'/html/head/link[contains(@href,"//cdn.shopify.com")]'
				]
			},
			'wix': {
				'headers': [],
				'body': [
					'/html/head/link[@href="https://www.wix.com"]'
				]
			},
			'squarespace': {
				'headers': [
					'server: Squarespace'
				],
				'body': [
					'/html/head/link[@href="https://images.squarespace-cdn.com"]',
					'/html/head/script[contains(@src,"//assets.squarespace.com")]'
				]
			}
		}

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
		if identifier == "wordpress":
			return "WordPress"
		elif identifier == "shopify":
			return "Shopify"
		else:
			return identifier.capitalize()
