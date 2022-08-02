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

	@property
	def address(self) -> str:
		"""Address property.

		Returns:
			[str]: Returns the address.
		"""
		return self._address

	@property
	def priority(self) -> int:
		"""Priority property.

		Returns:
			[int]: Returns the priority.
		"""
		return self._priority

	@property
	def text(self) -> tuple:
		"""Text property.

		Returns:
			[tuple]: Returns the text.
		"""
		return self._text

	@address.setter
	def address(self, address: str) -> None:
		"""Address property.

		Args:
			address (str): Sets the address.
		"""
		self._address = address

	@priority.setter
	def priority(self, priority: int) -> None:
		"""Priority property.

		Args:
			priority (int): Sets the priority.
		"""
		self._priority = priority

	@text.setter
	def text(self, text: tuple) -> None:
		"""Text property.

		Args:
			text (tuple): Sets the text.
		"""
		self._text = text

	def asdict(self) -> dict:
		"""Converts the Python object into a generic dictionary.

		Returns:
			[dict]: Generic dictionary representation.
		"""
		rtn = {}
		if len(self.address) > 0:
			rtn['address'] = self.address
		if self.priority > 0:
			rtn['priority'] = self.priority
		if len(self.text) > 0:
			rtn['text'] = self.text

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
		"""Success property.

		Returns:
			[bool]: Returns the success.
		"""
		return self._success

	@property
	def url(self) -> str:
		"""URL property.

		Returns:
			[str]: Returns the URL.
		"""
		return self._url

	@property
	def type(self) -> str:
		"""Type property.

		Returns:
			[str]: Returns the type.
		"""
		return self._type

	@property
	def records(self) -> [DNSResult]:
		"""Records property.

		Returns:
			[DNSResult]: Returns the records collection.
		"""
		return self._records

	@success.setter
	def success(self, success: bool) -> None:
		"""Success property.

		Args:
			success (bool): Sets the success.
		"""
		self._success = success

	@url.setter
	def url(self, url: str) -> None:
		"""URL property.

		Args:
			url (str): Sets the URL.
		"""
		self._url = url

	@type.setter
	def type(self, look_type: str) -> None:
		"""Type property.

		Args:
			look_type (str): Sets the type.
		"""
		self._type = look_type

	@records.setter
	def records(self, records: [DNSResult]) -> None:
		"""Records property.

		Args:
			records (DNSResult): Sets the DNS result collection.
		"""
		self._records = records

	def asdict(self) -> dict:
		"""Converts the Python object into a generic dictionary.

		Returns:
			[dict]: Generic dictionary representation.
		"""
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
	def probe(self, protocol:str, url:str) -> DNSResponse:
		"""
		Args:
			protocol (str): DNS Record type to lookup.
			url (str): Domain to check the records of.

		Returns:
			[DNSResponse]: The collective data.
		"""
		protocol = protocol.upper()
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
				if protocol in ('A', 'AAAA'):
					segment.address = data.address
				elif protocol in ('CNAME', 'NS'):
					segment.address = str(data.target)
				elif protocol == 'MX':
					segment.address = str(data.exchange)
					segment.priority = data.preference
				elif protocol == 'TXT':
					segment.text = data.strings

				respo.records.append(segment)

		respo.success = True

		return respo
