from typing import Optional
import urllib3, json

class WordPressIdentifier(object):
	def __init__(self, url):
		self.reply       = WordPress()
		self.pm          = urllib3.PoolManager()
		self.url         = url
		self.response    = None
		self.supports_v2 = False

	def get(self):
		"""Creates a collection of information scraped form the WordPress REST API.

		Returns:
			WordPress: Returns a WordPress object constructed from the class-defined URL.
		"""
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

		if self.supports_v2:
			self.page_stats()
			self.category_stats()

		return self.reply

	def page_stats(self) -> None:
		"""Collects information about the WordPress site posts and pages.
		"""
		response_posts = self.get_from_api(self.url + '/wp/v2/posts')
		response_pages = self.get_from_api(self.url + '/wp/v2/pages')

		if response_posts is not None:
			self.reply.post_count = int(response_posts['headers']['X-WP-Total'])

			if len(response_posts['api'][0]) > 0:
				post = Post()
				post.title = response_posts['api'][0]['title']['rendered']
				post.date  = response_posts['api'][0]['date']
				post.url   = response_posts['api'][0]['link']

				self.reply.latest_post = post

		if response_pages is not None:
			self.reply.page_count = int(response_pages['headers']['X-WP-Total'])

			if len(response_pages['api'][0]) > 0:
				page = Post()
				page.title = response_pages['api'][0]['title']['rendered']
				page.date  = response_pages['api'][0]['date']
				page.url   = response_pages['api'][0]['link']

				self.reply.latest_page = page

	def category_stats(self) -> None:
		"""Collects information about the site categories.
		"""
		response = self.get_from_api(self.url + '/wp/v2/categories')

		if response is not None:
			self.reply.cat_count = int(response['headers']['X-WP-Total'])


	def get_from_api(self, url: str) -> Optional[dict]:
		"""Contacts a WordPress REST API endpoint, and returns header and data responses.

		Args:
			url (str): URL to request (ignores self.url since this is for sub-requests).

		Returns:
			Optional[dict]: 'headers' is a list of headers, and 'api' is JSON content. None if an error occurs.
		"""
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
		self._success     = False
		self._name        = ''
		self._tagline     = ''
		self._timezone    = ''
		self._post_count  = -1
		self._page_count  = -1
		self._cat_count   = -1
		self._latest_post = None
		self._latest_page = None

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

	@property
	def latest_post(self):
		return self._latest_post

	@property
	def latest_page(self):
		return self._latest_page

	@success.setter
	def success(self, state) -> None:
		self._success = state

	@name.setter
	def name(self, name: str) -> None:
		self._name = name

	@tagline.setter
	def tagline(self, tagline: str) -> None:
		self._tagline = tagline

	@timezone.setter
	def timezone(self, timezone: str) -> None:
		self._timezone = timezone

	@post_count.setter
	def post_count(self, count: int) -> None:
		self._post_count = count

	@page_count.setter
	def page_count(self, count: int) -> None:
		self._page_count = count

	@cat_count.setter
	def cat_count(self, count: int) -> None:
		self._cat_count = count

	@latest_post.setter
	def latest_post(self, post) -> None:
		self._latest_post = post

	@latest_page.setter
	def latest_page(self, page) -> None:
		self._latest_page = page

	def asdict(self) -> dict:
		return {
			'success': self.success,
			'name': self.name,
			'tagline': self.tagline,
			'timezone': self.timezone,
			'post_count': self.post_count,
			'page_count': self.page_count,
			'cat_count': self.cat_count,
			'latest_post': self.latest_post.asdict() if self.latest_post is not None else None,
			'latest_page': self.latest_page.asdict() if self.latest_page is not None else None,
		}

class Post(object):
	def __init__(self):
		self._title = ''
		self._date  = ''
		self._url   = ''

	@property
	def title(self) -> str:
		return self._title

	@property
	def date(self) -> str:
		return self._date

	@property
	def url(self) -> str:
		return self._url

	@title.setter
	def title(self, title: str) -> None:
		self._title = title

	@date.setter
	def date(self, date: str) -> None:
		self._date = date

	@url.setter
	def url(self, url: str) -> None:
		self._url = url

	def asdict(self) -> dict:
		return {
			'title': self.title,
			'date': self.date,
			'url': self.url,
		}
