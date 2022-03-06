import urllib3
from lxml import html

class Inspection(object):
	def __init__(self, url):
		self.pm     = urllib3.PoolManager()
		self.url    = url
		self.parsed = None

		self.cms    = "N/A"
		self.wp_api = None

	def get_site_details(self):
		request = self.pm.request('GET', self.url)

		if request.status != 200:
			raise Exception("Site did not respond with a successful connection.")

		self.parsed = html.fromstring( request.data )#.decode('utf-8') )

		self.check_wordpress()

		return {
			'technology': self.cms
		}

	def check_wordpress(self):
		checkpoints = [
			'/html/head/link[@rel="https://api.w.org/"]',
			'/html/head/link[@href="//s.w.org"]',
			'//*[@id="wp-custom-css"]'
		]

		is_wp = False
		for check in checkpoints:
			hits = self.parsed.xpath(check)

			if len(hits) > 0:
				is_wp = True
				break
		
		if is_wp:
			try:
				self.wp_api = self.parsed.xpath('/html/head/link[@rel="https://api.w.org/"]')[0].attrib['href']
			except IndexError:
				pass
			
			self.cms = "WordPress"

			return True
		else:
			return False
		