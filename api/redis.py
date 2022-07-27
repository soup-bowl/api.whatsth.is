from os import getenv
import redis.asyncio as redis

async def init_redis_pool() -> redis.Redis:
	redis_c = await redis.from_url(
		getenv("REDIS_URL", "redis://localhost"),
		encoding="utf-8",
		decode_responses=True,
	)

	return redis_c

class CacheService:
	def __init__(self, redis: redis.Redis):
		self._redis = redis

	async def get_value(self, key: str):
		return await self._redis.get(key)
	
	async def set_value(self, key: str, value: str, timeout: int = 2592000):
		return await self._redis.set(key, value, ex=timeout)
