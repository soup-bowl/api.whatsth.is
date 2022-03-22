from typing import Optional
from api.objects.inspectionresult import InspectionResult

class APIResponse(object):
	def __init__(self):
		self._success    = False
		self._message    = ''
		self._inspection = None
		self._url        = ''

	@property
	def success(self) -> bool:
		return self._success
	
	@property
	def message(self) -> str:
		return self._message

	@property
	def inspection(self) -> Optional[InspectionResult]:
		return self._inspection
	
	@property
	def url(self) -> str:
		return self._url
	
	@success.setter
	def success(self, success: bool):
		self._success = success
		return self
	
	@message.setter
	def message(self, message: str):
		self.message = message
		return self
	
	@inspection.setter
	def inspection(self, inspection: InspectionResult = None):
		self._inspection = inspection
		return self

	@url.setter
	def url(self, url: str):
		self._url = url
		return self
