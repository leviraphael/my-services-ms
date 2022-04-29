import redis
from redis import Redis

REDIS_SERVER = 'services.redis.cache.windows.net'
REDIS_PORT = 6380
# TODO remove password from repo
REDIS_PASSWORD = '3rm7WM7u4oBh8uAM1l584oZir1dX58p4HAzCaHLmnLY='


class RedisUtil:

    def connect_to_redis(self) -> Redis:
        return redis.Redis(
            host=REDIS_SERVER,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            ssl=True)

    def clear_all_keys(self, r: Redis):
        return [r.delete(key) for key in r.keys()]
