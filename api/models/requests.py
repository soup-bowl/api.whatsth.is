from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session

from api.models.database import Base

class Requests(Base):
	__tablename__ = "requests"

	id = Column(Integer, primary_key=True, index=True)
	ipaddr = Column(String)
	url = Column(String)
	time = Column(DateTime)

class RequestsService(object):
	def __init__(self, db: Session):
		self.db = db
	
	def getRequestFrequency(self) -> dict:
		return {
			"week": self.db.query(Requests).filter(Requests.time >= (datetime.now() - timedelta(days=7))  ).count(),
			"month": self.db.query(Requests).filter(Requests.time >= (datetime.now() - timedelta(days=30)) ).count(),
			"quarter": self.db.query(Requests).filter(Requests.time >= (datetime.now() - timedelta(days=90)) ).count(),
			"year": self.db.query(Requests).filter(Requests.time >= (datetime.now() - timedelta(days=365))).count(),
		}

	def setInfo(self, url: str) -> Requests:
		info = Requests(url=url, time=datetime.now())
		self.db.add(info)
		self.db.commit()
		self.db.refresh(info)
		return info
