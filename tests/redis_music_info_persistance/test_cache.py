from redis_cache.redis_cache import RedisCache
from redis_cache.rediscache import cache_it

redisAddress = "127.0.0.1"
redisPort = 0
redisCache = RedisCache(redisAddress, redisPort)
redisExpire = 

@cache_it(limit=3, expire=redisExpire)
def test_function(parameter):
    print('hello world')
    print('parameter:',parameter)
    return 'abcdefg'

