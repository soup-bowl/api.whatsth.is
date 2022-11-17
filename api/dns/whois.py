import datetime
from typing import Union
from whois import whois
from whois.parser import PywhoisError

class WhoisResult():
	"""Object representing an individual lookup response.
	"""
	@property
	def domain(self) -> str:
		"""Domain name being inspected.

		Returns:
			[str]: Domain name (from whois).
		"""
		return self._domain

	@property
	def registrar(self) -> str:
		"""Registar company name.

		Returns:
			[str]: Company name.
		"""
		return self._registrar

	@property
	def whois_operator(self) -> str:
		"""Whois lookup URL.

		Returns:
			[str]: whois URL.
		"""
		return self._whois_operator

	@property
	def nameservers(self) -> list:
		"""Nameservers associated with the domain.

		Returns:
			[list]: URLs.
		"""
		return self._nameservers

	@property
	def date_created(self) -> datetime:
		"""First registration date.

		Returns:
			[datetime]: Date.
		"""
		return self._date_created

	@property
	def date_updated(self) -> datetime:
		"""Last re-registration date.

		Returns:
			[datetime]: Date.
		"""
		return self._date_updated

	@property
	def date_expires(self) -> datetime:
		"""Lease expiration date.

		Returns:
			[datetime]: Date.
		"""
		return self._date_expires

	@domain.setter
	def domain(self, url: str) -> None:
		"""Domain name being inspected.

		Args:
			url (str): Domain name (from whois).
		"""
		self._domain = url

	@registrar.setter
	def registrar(self, registrar: str) -> None:
		"""Registar company name.

		Args:
			registrar (str): Company name.
		"""
		self._registrar = registrar

	@whois_operator.setter
	def whois_operator(self, whois: str) -> None:
		"""Whois lookup URL.

		Args:
			whois (str): whois URL.
		"""
		self._whois_operator = whois

	@nameservers.setter
	def nameservers(self, ns: list) -> None:
		"""Nameservers associated with the domain.

		Args:
			ns (list): URLs.
		"""
		self._nameservers = ns

	@date_created.setter
	def date_created(self, date_created: datetime) -> None:
		"""First registration date.

		Args:
			date_created (datetime): Date.
		"""
		self._date_created = date_created

	@date_updated.setter
	def date_updated(self, date_updated: datetime) -> None:
		"""Last re-registration date.

		Args:
			date_updated (datetime): Date.
		"""
		self._date_updated = date_updated

	@date_expires.setter
	def date_expires(self, date_expires: datetime) -> None:
		"""Lease expiration date.

		Args:
			date_expires (datetime): Date.
		"""
		self._date_expires = date_expires

	def asdict(self) -> dict:
		"""Converts the Python object into a generic dictionary.

		Returns:
			[dict]: Generic dictionary representation.
		"""
		return {
			'domain': self.domain,
			'registrar': self.registrar,
			'whois_operator': self.whois_operator,
			'nameservers': self.nameservers,
			'date_created': self.date_created.isoformat(),
			'date_updated': self.date_updated.isoformat(),
			'date_expires': self.date_expires.isoformat()
		}

class WhoisLookup():
	"""Service class to communicate with registrar whois lookups.
	"""
	def lookup(self, url:str) -> Union[WhoisResult, str]:
		"""
		Args:
			url (str): Domain to lookup.

		Returns:
			Union[WhoisResult, str]: The collective data, or an error message.
		"""
		try:
			r = whois(url)
		except PywhoisError:
			return "Domain could not be found."

		if r.domain_name is None:
			return "No discernible domain specified, or an unsupported TLD was requested."

		o = WhoisResult()
		o.domain = r.domain_name if not isinstance(r.domain_name, list) else r.domain_name[0]
		o.registrar = r.registrar
		o.whois_operator = r.whois_server
		o.nameservers = r.name_servers
		o.date_created = r.creation_date if not isinstance(r.creation_date, list) else r.creation_date[0]
		o.date_updated = r.updated_date if not isinstance(r.updated_date, list) else r.updated_date[0]
		o.date_expires = r.expiration_date if not isinstance(r.expiration_date, list) else r.expiration_date[0]

		return o
