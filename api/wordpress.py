from pickle import FALSE
from urllib import response
import urllib3, unicodedata, re, json
from os import remove
from os.path import exists, getmtime
from pathlib import Path
from time import time

class WordPress(object):
	def __init__(self, url):
		self.pm       = urllib3.PoolManager()
		self.url      = url
		self.response = None

	def get(self):
		request = self.pm.request('GET', self.url)

		if request.status != 200:
			return {
				'status': 'fail',
			}

		self.response = json.loads(request.data.decode('utf-8'))

		return {
			'status': 'success',
			'name': self.response['name'],
			'tagline': self.response['description'],
			'timezone': self.response['timezone_string'],
			'content': self.page_stats()
		}
	
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
