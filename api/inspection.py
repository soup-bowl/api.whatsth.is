import urllib3
from lxml import html

class Inspection(object):
	def __init__(self, url):
		self.pm     = urllib3.PoolManager()
		self.url    = url
		self.parsed = None

		self.cms    = "N/A"
		self.match  = None
		self.wp_api = None

	def get_site_details(self):
		request = self.pm.request('GET', self.url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0'})

		if request.status != 200:
			raise Exception(str(request.status) + " - Site did not respond with a successful connection.")

		self.parsed = html.fromstring( request.data )#.decode('utf-8') )

		self.identifty_cms()

		return {
			'technology': self.cms
		}
	
	def identifty_cms(self):
		checkpoints = {
			'wordpress': [
				'/html/head/link[@rel="https://api.w.org/"]',
				'/html/head/link[@href="//s.w.org"]',
				'//*[@id="wp-custom-css"]'
			]
		}

		for check in checkpoints['wordpress']:
			hits = self.parsed.xpath(check)
			if len(hits) > 0:
				self.match = check
				self.cms   = "WordPress"

				try:
					self.wp_api = self.parsed.xpath('/html/head/link[@rel="https://api.w.org/"]')[0].attrib['href']
				except IndexError:
					pass

				return
