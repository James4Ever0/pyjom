# saucenao (if fail, use trace.moe)
# use proxies, since we are using free tiers.
import os
SAUCENAO_API_KEY=os.environ.get('SAUCENAO_API_KEY') # how to run this without api key?
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
    best = results[0]
    similarity = best.similarity
    # just trust anilist.
    urls = best.urls # https://anilist.co/anime/ https://anidb.net/anime/ https://myanimelist.net/anime/
    best_data =  best.raw.get('data',{})
    part = best_data.get('part', None) # not always.
    title = best.title
    est_time =best_data.get('est_time',None) # be like: '00:16:21 / 00:25:12'
    if est_time:
        start_end = [timestamp.strip() for timestamp in est_time.split("/")]
        start_time, end_time = start_end
    # these ids must be the same across different images.
    anidb_aid = best_data.get('anidb_aid',None)
    mal_id = best_data.get('mal_id',None)
    anilist_id = best_data.get('anilist_id',None)
    breakpoint()
