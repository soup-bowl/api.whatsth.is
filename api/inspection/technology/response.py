"""Inspection API response.
"""

from typing import Optional

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
		return self._success

	@property
	def message(self) -> str:
		return self._message

	@property
	def inspection(self) -> Optional[object]:
		return self._inspection

	@property
	def url(self) -> str:
		return self._url

	@success.setter
	def success(self, success: bool) -> None:
		self._success = success

	@message.setter
	def message(self, message: str) -> None:
		self._message = message

	@inspection.setter
	def inspection(self, inspection: object = None) -> None:
		self._inspection = inspection

	@url.setter
	def url(self, url: str) -> None:
		self._url = url

	def asdict(self) -> dict:
		return {
			'success': self.success,
			'message': self.message if self.inspection is None else self.inspection,
			'url': self.url,
		}
