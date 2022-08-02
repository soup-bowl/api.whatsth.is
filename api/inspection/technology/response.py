"""Inspection API response.
"""

from typing import Optional

from api.inspection.inspection import InspectionResult

class APIResponse():
	"""Inspection interaction functionality.
	"""
	def __init__(self):
		self._success = False
		self._message = ''
		self._inspection = None
		self._url = ''

	@property
	def success(self) -> bool:
		"""Success property.

		Returns:
			[bool]: Returns the success.
		"""
		return self._success

	@property
	def message(self) -> str:
		"""Message property.

		Returns:
			[str]: Returns the message.
		"""
		return self._message

	@property
	def inspection(self) -> Optional[InspectionResult]:
		"""Inspection result property.

		Returns:
			[InspectionResult]: Returns the inspection result.
		"""
		return self._inspection

	@property
	def url(self) -> str:
		"""URL property.

		Returns:
			[str]: Returns the URL.
		"""
		return self._url

	@success.setter
	def success(self, success: bool) -> None:
		"""Success property.

		Args:
			success (bool): Sets the success.
		"""
		self._success = success

	@message.setter
	def message(self, message: str) -> None:
		"""Message property.

		Args:
			message (str): Sets the message.
		"""
		self._message = message

	@inspection.setter
	def inspection(self, inspection: InspectionResult = None) -> None:
		"""Inspection result property.

		Args:
			inspection (InspectionResult): Sets the inspection result.
		"""
		self._inspection = inspection

	@url.setter
	def url(self, url: str) -> None:
		"""URL property.

		Args:
			url (str): Sets the URL.
		"""
		self._url = url

	def asdict(self) -> dict:
		"""Converts the Python object into a generic dictionary.

		Returns:
			[dict]: Generic dictionary representation.
		"""
		return {
			'success': self.success,
			'message': self.message if self.inspection is None else self.inspection,
			'url': self.url,
		}
