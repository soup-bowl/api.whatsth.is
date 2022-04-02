import hashlib, pickle
from datetime import datetime, timedelta
from typing import Any, Optional
from sqlalchemy import Column, Integer, String, DateTime, BLOB
from sqlalchemy.orm import Session

from api.models.database import Base

class RequestCache(Base):
	__tablename__ = "requestcache"

	id        = Column(Integer, primary_key=True, index=True)
	reference = Column(String, unique=True, index=True)
	cache     = Column(BLOB)
	expiry    = Column(DateTime)

class RequestCacheService(object):
	def __init__(self, db: Session):
		self.db = db

	def getCachedInspection(self, reference: str) -> Optional[RequestCache]:
		check    = hashlib.md5(reference.encode('utf-8')).hexdigest()
		response = self.db.query(RequestCache).filter(RequestCache.reference == check).first()

		if response is not None:
			decoded = pickle.loads(response.cache)

			if datetime.now() > response.expiry:
				self.db.query(RequestCache).filter(RequestCache.id == response.id).delete()
				self.db.commit()

				return None

			return decoded

		return None

	def setCachedInspection(self, reference: str, contents: Any) -> RequestCache:
		pickled = pickle.dumps(contents, pickle.HIGHEST_PROTOCOL)
		check   = hashlib.md5(reference.encode('utf-8')).hexdigest()
		cache   = RequestCache(reference=check, cache=pickled, expiry=(datetime.now() + timedelta(days=30)))
		self.db.add(cache)
		self.db.commit()
		self.db.refresh(cache)
		return cache
