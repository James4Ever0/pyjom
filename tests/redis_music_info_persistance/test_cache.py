from redis_cache.redis_cache import RedisCache
from redis_cache.rediscache import cache_it


redisCache = RedisCache(redisAddress, redisPort)

def test_function(parameter):
    print('hello world')
    print('parameter:',parameter)
    return 'abcdefg'

