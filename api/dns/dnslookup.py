"""DNS lookup functionality.
"""

import dns.resolver
from urllib3.util import parse_url
from dns.resolver import NoAnswer

class DNSResult():
	"""Object representing an individual lookup response.
	"""
	def __init__(self):
		self._address = ''
		self._priority = 0
		self._text = []
		self._ttl = 0

	@property
	def address(self) -> str:
		return self._address

	@property
	def priority(self) -> int:
		return self._priority

	@property
	def text(self) -> tuple:
		return self._text

	@property
	def ttl(self) -> int:
		return self._ttl

	@address.setter
	def address(self, address: str) -> None:
		self._address = address

	@priority.setter
	def priority(self, priority: int) -> None:
		self._priority = priority

	@text.setter
	def text(self, text: tuple) -> None:
		self._text = text

	@ttl.setter
	def ttl(self, ttl: int) -> None:
		self._ttl = ttl

	def asdict(self) -> dict:
		rtn = {}
		if len(self.address) > 0:
			rtn['address'] = self.address
		if self.priority > 0:
			rtn['priority'] = self.priority
		if len(self.text) > 0:
			rtn['text'] = []
			for text in self.text:
				rtn['text'].append(text.decode('UTF-8'))
		rtn['ttl'] = self.ttl

		return rtn

class DNSResponse():
	"""Represents a collection of DNS lookup records.
	"""
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
	def type(self, look_type: str) -> None:
		self._type = look_type

	@records.setter
	def records(self, records: [DNSResult]) -> None:
		self._records = records

	def asdict(self) -> dict:
		records = []
		for items in self.records:
			records.append(items.asdict())

		return {
			'success': self.success,
			'url': self.url,
			'type': self.type,
			'records': records,
		}

class DNSLookup():
	"""Service class to interact with DNS functionality.
	"""

	@staticmethod
	def supported_protocols() -> list:
		"""Supported protocols by the DNS lookup utility.

		Returns:
			[list]: Returns a dict list of 'type' and 'name'.
		"""
		return [
			{ 'type': 'A', 'name': 'Address (IPv4)' },
			{ 'type': 'AAAA', 'name': 'Address (IPv6)' },
			{ 'type': 'CNAME', 'name': 'Canonical Name' },
			{ 'type': 'MX', 'name': 'Mail Exchange' },
			{ 'type': 'NS', 'name': 'Name Server' },
			{ 'type': 'TXT', 'name': 'Text' }
		]

	def probe_all(self, url:str) -> DNSResponse:
		"""
		Args:
			url (str): Domain to check the records of.

		Returns:
			[DNSResponse]: The collective data.
		"""
		domain = parse_url(url).netloc
		record_types = ['A', 'MX', 'CNAME', 'TXT', 'NS']
		respo = {
			'success': True,
			'message': None,
			'records': {
				'A': [],
				'AAAA': [],
				'CNAME': [],
				'MX': [],
				'TXT': [],
				'NS': [],
			}
		}

		for record_type in record_types:
			try:
				answers = dns.resolver.query(domain, record_type)

				for answer in answers:
					if record_type == 'A' and hasattr(answer, 'address'):
						respo['records']['A'].append(answer.address)
					elif record_type == 'AAAA' and hasattr(answer, 'address'):
						respo['records']['AAAA'].append(answer.address)
					elif record_type == 'CNAME' and hasattr(answer, 'target'):
						respo['records']['CNAME'].append(str(answer.target))
					elif record_type == 'NS' and hasattr(answer, 'target'):
						respo['records']['NS'].append(str(answer.target))
					elif record_type == 'MX' and hasattr(answer, 'exchange'):
						respo['records']['MX'].append({
							'address': str(answer.exchange),
							'priority': answer.preference
						})
					elif record_type == 'TXT' and hasattr(answer, 'strings'):
						respo['records']['TXT'].append(answer.strings[0].decode('utf-8'))

			except dns.resolver.NoAnswer:
				pass
			except dns.resolver.NXDOMAIN:
				respo['success'] = False
				respo['message'] = f"Domain {domain} does not exist"
				return respo
			except dns.resolver.NoNameservers:
				respo['success'] = False
				respo['message'] = f"No nameservers found for {domain}"
				return respo

		return respo
	
	def _segment_response(self, protocol:str, data) -> DNSResult:
		"""Stores the response DNS data into the relevant data fields.

		Args:
			protocol (str): DNS Record type to lookup.
			data (any): Data from the dnspython lookup.
		
		Returns:
			DNSResult: DNS result object.
		"""
		segment = DNSResult()

		# Definition for these - https://dnspython.readthedocs.io/en/latest/rdata-subclasses.html
		if protocol in ('A', 'AAAA'):
			segment.address = data.address
		elif protocol in ('CNAME', 'NS'):
			segment.address = str(data.target)
		elif protocol == 'MX':
			segment.address = str(data.exchange)
			segment.priority = data.preference
		elif protocol == 'TXT':
			segment.text = data.strings
			
		return segment

	def _discover_nameserver(self, url:str) -> list:
		"""Discover the nameserver of a domain.

		Args:
			url (str): Domain to check the records of.
		
		Returns:
			list: List of nameservers.
		"""
		topdom = '.'.join(url.split('.')[-2:])

		return dns.resolver.query(topdom, 'NS')
