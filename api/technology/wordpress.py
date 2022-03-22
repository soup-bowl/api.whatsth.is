from time import time
import urllib3, json

class WordPressIdentifier(object):
	def __init__(self, url):
		self.reply       = WordPress()
		self.pm          = urllib3.PoolManager()
		self.url         = url
		self.response    = None
		self.supports_v2 = False

	def get(self):
		request = self.pm.request('GET', self.url)

		if request.status != 200:
			return self.reply

		self.response = json.loads(request.data.decode('utf-8'))
		if 'wp/v2' in self.response['namespaces']:
			self.supports_v2 = True

		self.reply.success  = True
		self.reply.name     = self.response['name']
		self.reply.tagline  = self.response['description']
		self.reply.timezone = self.response['timezone_string']

		#if self.supports_v2:
		#	reply['content']    = self.page_stats()
		#	reply['categories'] = self.category_stats()

		return self.reply

	def page_stats(self):
		response_posts = self.get_from_api(self.url + '/wp/v2/posts')
		response_pages = self.get_from_api(self.url + '/wp/v2/pages')
		reply = {}

		if response_posts is not None:
			data = {
				'count': int(response_posts['headers']['X-WP-Total']),
			}

			if len(response_posts['api'][0]) > 0:
				data['latest'] = {
					'title': response_posts['api'][0]['title']['rendered'],
					'date':  response_posts['api'][0]['date'],
					'url':   response_posts['api'][0]['link']
				}
			else:
				data['latest'] = False

			reply['posts'] = data

		if response_pages is not None:
			data = {
				'count': int(response_pages['headers']['X-WP-Total']),
			}

			if len(response_pages['api'][0]) > 0:
				data['latest'] = {
					'title': response_pages['api'][0]['title']['rendered'],
					'date':  response_pages['api'][0]['date'],
					'url':   response_pages['api'][0]['link']
				}
			else:
				data['latest'] = False

			reply['pages'] = data

		return reply

	def category_stats(self):
		response = self.get_from_api(self.url + '/wp/v2/categories')
		if response is not None:
			reply = {
				'count': int(response['headers']['X-WP-Total']),
			}

		return reply


	def get_from_api(self, url):
		request = self.pm.request('GET', url)
		if request.status != 200:
			return None
		else:
			data = {
				'headers': request.headers,
				'api': json.loads(request.data.decode('utf-8'))
			}

			if len(data['api']) == 0:
				return None

			return data

class WordPress(object):
	def __init__(self):
		self._success    = False
		self._name       = ''
		self._tagline    = ''
		self._timezone   = ''
		self._post_count = -1
		self._page_count = -1
		self._cat_count  = -1

	@property
	def success(self) -> bool:
		return self._success

	@property
	def name(self) -> str:
		return self._name

	@property
	def tagline(self) -> str:
		return self._tagline

	@property
	def timezone(self) -> str:
		return self._timezone

	@property
	def post_count(self) -> int:
		return self._post_count

	@property
	def page_count(self) -> int:
		return self._page_count

	@property
	def cat_count(self) -> int:
		return self._cat_count

	@success.setter
	def success(self, state):
		self._success = state

	@name.setter
	def name(self, name):
		self._name = name

	@tagline.setter
	def tagline(self, tagline):
		self._tagline = tagline

	@timezone.setter
	def timezone(self, timezone):
		self._timezone = timezone

	@post_count.setter
	def post_count(self, count):
		self._post_count = count

	@page_count.setter
	def page_count(self, count):
		self._page_count = count

	@cat_count.setter
	def cat_count(self, count):
		self._cat_count = count

	def asdict(self):
		return {
			'success': self.success,
			'name': self.name,
			'tagline': self.tagline,
			'timezone': self.timezone,
			'post_count': self.post_count,
			'page_count': self.page_count,
			'cat_count': self.cat_count,
		}