# from redis_cache.redis_cache import RedisCache
# from redis_cache.rediscache import cache_it
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis()
cache = RedisLRU(client)

redisAddress = "127.0.0.1"
redisPort = 9291
# redisCache = RedisCache(redisAddress, redisPort)
oneDay = 60*60*24 # one day?
redisExpire =oneDay*7 # god damn it!

# @redisCache.cache(limit=3, expire=redisExpire)
# from functools import lru_cache

# @lru_cache(maxsize=2)
@cache(ttl=redisExpire)
def test_function(parameter):
    print('hello world')
    print('parameter:',parameter)
    return 'abcdefg'

print("RESULT:",test_function('toy_data'))
print("RESULT:",test_function('toy_data'))