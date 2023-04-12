""" Redis cache interactions handler.
"""

from os import getenv
from typing import Optional
import redis.asyncio as redis

from api import VERSION

async def init_redis_pool() -> redis.Redis:
	"""Instantiates the Redis cache worker pools.
	"""

	redis_c = await redis.from_url(
		getenv("REDIS_URL", "redis://localhost"),
		encoding="utf-8",
		decode_responses=True,
	)

	return redis_c

class CacheService:
	"""Redis interaction service.
	"""

	def __init__(self, redis_instance: redis.Redis):
		self._redis = redis_instance
		self._key_prefix = "wapi{ver}:".format(ver=VERSION.replace('.', ''))

	async def get_value(self, key: str):
		"""Gets a string value from the cache.

		Args:
			key (str): The key to lookup in the cache for.

		Return:
			[str]: The result of the lookup.
		"""
		return await self._redis.get(self._key_prefix + key)

	async def set_value(self, key: str, value: str, timeout: Optional[int] = None):
		"""Sets a value in the Redis cache.

		Args:
			key (str): The key to lookup in the cache for.
			value (str): What to set the value to.
			timeout (int): How long the value should persist for.
		"""
		return await self._redis.set(self._key_prefix + key, value, ex=timeout)
