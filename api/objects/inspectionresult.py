class InspectionResult(object):
	def __init__(self):
		self._technology  = 'Unknown'
		self._matched_on  = []
		self._match_count = 0
		self._match_total = 0
		self._additional  = None
	
	@property
	def technology(self) -> str:
		return self._technology
	
	@property
	def matched_on(self) -> list:
		return self._matched_on
	
	@property
	def match_count(self) -> int:
		return self._match_count
	
	@property
	def match_total(self) -> int:
		return self._match_total
	
	@property
	def additional(self):
		return self._additional
	
	@technology.setter
	def technology(self, technology: str):
		self._technology = technology
		return self
	
	@matched_on.setter
	def matched_on(self, matchedon: list):
		self._matched_on = matchedon
		return self
	
	@match_count.setter
	def match_count(self, count: int):
		self._match_count = count
		return self
	
	@match_total.setter
	def match_total(self, count: int):
		self._match_total = count
		return self
	
	@additional.setter
	def additional(self, additional):
		self._additional = additional
		return self
	
	def add_match(self, match_string):
		self._matched_on.append(match_string)
		self._match_count = self._match_count + 1
		return self
	
	def asdict(self):
		return {
			'technology': self.technology,
			'matched_on': self.matched_on,
			'additional': self.additional,
		}

