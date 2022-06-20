import dns.resolver
from urllib3.util import parse_url
from dns.resolver import NoAnswer

class DNSResult(object):
	def __init__(self):
		self._address = ''
		self._priority = 0
		self._text = []

	@property
	def address(self) -> str:
		return self._address

	@property
	def priority(self) -> int:
		return self._priority

	@property
	def text(self) -> tuple:
		return self._text

	@address.setter
	def address(self, address: str) -> None:
		self._address = address

	@priority.setter
	def priority(self, p: int) -> None:
		self._priority = p

	@text.setter
	def text(self, text: tuple) -> None:
		self._text = text

	def asdict(self) -> dict:
		rtn = {}
		if len(self.address) > 0:
			rtn['address'] = self.address
		if self.priority > 0:
			rtn['priority'] = self.priority
		if len(self.text) > 0:
			rtn['text'] = self.text

		return rtn

class DNSResponse(object):
	def __init__(self):
		self._success = False
		self._url = ''
		self._type = ''
		self._records = []

	@property
	def success(self) -> bool:
		return self._success

	@property
	def url(self) -> str:
		return self._url

	@property
	def type(self) -> str:
		return self._type

	@property
	def records(self) -> [DNSResult]:
		return self._records

	@success.setter
	def success(self, success: bool) -> None:
		self._success = success

	@url.setter
	def url(self, url: str) -> None:
		self._url = url

	@type.setter
	def type(self, type: str) -> None:
		self._type = type

	@records.setter
	def records(self, records: [DNSResult]) -> None:
		self._records = records

	def asdict(self) -> dict:
		r = []
		for items in self.records:
			r.append(items.asdict())

		return {
			'success': self.success,
			'url': self.url,
			'type': self.type,
			'records': r,
		}

class DNSLookup(object):
	def probe(self, protocol:str, url:str) -> DNSResponse:
		respo = DNSResponse()
		respo.url = parse_url(url).netloc
		respo.type = protocol

		none_found = False
		try:
			lookup = dns.resolver.resolve(respo.url, protocol)
		except NoAnswer:
			none_found = True

		if not none_found:
			for data in lookup:
				segment = DNSResult()

				# Definition for these - https://dnspython.readthedocs.io/en/latest/rdata-subclasses.html
				if (protocol == 'A' or protocol == 'AAAA'):
					segment.address = data.address
				if (protocol == 'CNAME'):
					segment.address = str(data.target)
				elif (protocol == 'MX'):
					segment.address  = str(data.exchange)
					segment.priority = data.preference
				elif (protocol == 'NS'):
					segment.address = str(data.target)
				elif (protocol == 'TXT'):
					segment.text = data.strings

				respo.records.append(segment)

		respo.success = True

		return respo
