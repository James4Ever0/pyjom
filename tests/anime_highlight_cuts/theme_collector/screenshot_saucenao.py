# saucenao (if fail, use trace.moe)
# use proxies, since we are using free tiers.
import os
SAUCENAO_API_KEY=os.environ.get('SAUCENAO_API_KEY')
print("API KEY?", SAUCENAO_API_KEY)

# sauce = SauceNao(api_key=SAUCENAO_API_KEY) # shit. not working!
filepath = "/Users/jamesbrown/Downloads/anime_download/dress_test_pictures/女装0.jpeg"
# import asyncio
# loop = asyncio.get_event_loop()
# results = loop.run_until_complete(sauce.from_file(filepath))
# results = await sauce.from_url('https://i.imgur.com/QaKpV3s.png')
# no api key. fuck.
from saucenao_api import SauceNao
sauce = SauceNao(SAUCENAO_API_KEY)
with open(filepath,'rb') as f:
    results = sauce.from_file(f)
    long_remaining = results.long_remaining # wait till next day? wtf?
    short_remaining = results.short_remaining
    result_results = len(results)
    print(results)
    breakpoint()
    best = results[0]
    urls = best.urls