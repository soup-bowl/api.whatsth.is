import hashlib
import pickle
from time import time
from datetime import datetime, timedelta
from typing import Any
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BLOB
from sqlalchemy.orm import relationship, Session

from api.database import Base, SessionLocal

class RequestCache(Base):
	__tablename__ = "requestcache"

	id        = Column(Integer, primary_key=True, index=True)
	reference = Column(String, unique=True, index=True)
	cache     = Column(BLOB)
	expiry    = Column(DateTime)

class RequestCacheService(object):
	def __init__(self, db):
		self.db = db

	def getCachedInspection(self, reference: str):
		check    = hashlib.md5(reference.encode('utf-8')).hexdigest()
		response = self.db.query(RequestCache).filter(RequestCache.reference == check).filter(RequestCache.expiry > datetime.now()).first()

		if response is not None:
			decoded = pickle.loads(response.cache)
			return decoded

		return None

	def setCachedInspection(self, reference: str, contents: Any):
		pickled = pickle.dumps(contents, pickle.HIGHEST_PROTOCOL)
		check   = hashlib.md5(reference.encode('utf-8')).hexdigest()
		cache   = RequestCache(reference=check, cache=pickled, expiry=(datetime.now() + timedelta(days=30)))
		self.db.add(cache)
		self.db.commit()
		self.db.refresh(cache)
		return cache
