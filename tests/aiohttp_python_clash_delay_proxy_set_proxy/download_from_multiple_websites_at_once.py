import aiohttp
import asyncio

# clearly it is not clean enough.
# also i worry about the memory leakage, open file limit exceeding.
async def get(url, processor=lambda x: x, params={}):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await processor(response)
            return result


def concurrentGet(url_list, processor=lambda x: x, params={}, debug=False):
    loop = asyncio.get_event_loop()
    multiple_requests = [
        get(url, processor=processor, params=params) for url in url_list
    ]
    results = loop.run_until_complete(asyncio.gather(*multiple_requests))
    if debug:
        print("Results: %s" % results)
    return results
