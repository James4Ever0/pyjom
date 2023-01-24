# saucenao (if fail, use trace.moe)
# use proxies, since we are using free tiers.
from pysaucenao import SauceNao
sauce = SauceNao()
filepath = "/Users/jamesbrown/Downloads/anime_download/dress_test_pictures/女装0.jpeg"
results = await sauce.from_file(filepath)
# results = await sauce.from_url('https://i.imgur.com/QaKpV3s.png')
print(results)