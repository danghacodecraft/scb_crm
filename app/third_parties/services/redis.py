import aioredis
from loguru import logger

from app.utils.functions import orjson_dumps, orjson_loads


class ServiceRedis:
    redis = None
    service_name = "REDIS"

    def __init__(self, init_service):
        self.init_service = init_service

    def start(self):
        logger.info("Start Call Redis")
        init_service = self.init_service
        self.redis = aioredis.from_url(
            f"redis://{init_service['REDIS']['REDIS_HOST']}:{init_service['REDIS']['REDIS_PORT']}",
            password=init_service['REDIS']['REDIS_PASSWORD'],
            db=init_service['REDIS']['REDIS_DATABASE']
        )

    async def stop(self):
        await self.redis.close()
        logger.info("Stop Redis")
        return None

    async def get(self, key) -> str:
        """
        Lấy giá trị lưu trữ bởi key
        """
        logger.log("SERVICE", f"[{self.service_name}] GET {key}")
        return orjson_loads(await self.redis.get(key))

    async def getset(self, key, value):
        """
        Lấy ra giá trị cũ và đặt giá trị mới cho key
        """
        logger.log("SERVICE", f"[{self.service_name}] GET SET {key}")
        await self.redis.getset(key, orjson_dumps(value))
