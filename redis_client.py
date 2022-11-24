import aioredis
from config import REDIS_HOST, REDIS_PORT


class RedisClient:

    def __init__(self):
        self.client = self._get_redis_client()

    @staticmethod
    def _get_redis_client():
        try:
            client = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=5, decode_responses=True)
            ping = client.ping()
            if ping:
                return client
            raise Exception
        except aioredis.AuthenticationError:
            print("Ошибка подключения к Redis")
            raise aioredis.AuthenticationError
        except Exception as e:
            print(e)
            raise Exception 

    def _create_caching_key(self, user_tg_id):
        return f"{user_tg_id}"


    async def cache_user_data(self, user_tg_id, data):
        key = self._create_caching_key(user_tg_id)
        await self.client.hmset(key, data)

    async def get_user_data(self, user_tg_id):
        key = self._create_caching_key(user_tg_id)
        return await self.client.hgetall(key)

    async def del_user_data(self, user_tg_id):
        key = self._create_caching_key(user_tg_id)
        await self.client.delete(key)

    def _create_film_key(self, user_tg_id): 
        return f"film_{user_tg_id}"
     
    async def cache_user_film(self, user_tg_id, data):
        key = self._create_film_key(user_tg_id)
        await self.client.hmset(key, data)
    
    async def get_user_film(self, user_tg_id):
        key = self._create_film_key(user_tg_id)
        return await self.client.hgetall(key)
    
    async def delete_user_film(self, user_tg_id):
        key = self._create_film_key(user_tg_id)
        await self.client.delete(key)



redis_client = RedisClient()
