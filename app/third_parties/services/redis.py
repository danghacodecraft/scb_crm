import aioredis
from loguru import logger

from app.settings.service import SERVICE
from app.utils.functions import orjson_dumps, orjson_loads


class ServiceRedis:
    redis = None
    service_name = "REDIS"

    def start(self):
        logger.info("Start Call Redis")
        self.redis = aioredis.from_url(
            f"redis://{SERVICE['redis']['host']}:{SERVICE['redis']['port']}",
            password=SERVICE['redis']['password'],
            db=SERVICE['redis']['database']
        )

    async def stop(self):
        await self.redis.close()
        logger.info("Stop Redis")
        return None

    async def get(self, key) -> str:
        logger.log("SERVICE", f"[{self.service_name}] GET {key}")
        return orjson_loads(await self.redis.get(key))

    async def set(self, key, value):
        logger.log("SERVICE", f"[{self.service_name}] SET {key}")
        await self.redis.set(key, orjson_dumps(value))
