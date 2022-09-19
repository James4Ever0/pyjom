# from redis_cache.redis_cache import RedisCache
# from redis_cache.rediscache import cache_it
import redis
from redis_lru import RedisLRU

from functools import lru_cache
oneDay = 60*60*24 # one day?
redisExpire =oneDay*7 # god damn it!

@lru_cache(maxsize=1)
def redisLRUCache(ttl=redisExpire,redisAddress = "127.0.0.1",redisPort = 9291,max_size=20):
    client = redis.StrictRedis(host=redisAddress, port=redisPort)
    cache = RedisLRU(client,max_size=max_size)
    return cache(ttl=redisExpire)

# we've fixed this shit.
@redisLRUCache()
def test_function(parameter):
    print('hello world')
    print('parameter:',parameter)
    return 'abcdefg'

print("RESULT:",test_function('toy_data'))
print("RESULT:",test_function('toy_data'))