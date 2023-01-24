# saucenao (if fail, use trace.moe)
# use proxies, since we are using free tiers.
from pysaucenao import SauceNao
sauce = SauceNao()

# results = await sauce.from_file('/path/to/image.png')
results = await sauce.from_url('https://i.imgur.com/QaKpV3s.png')
repr(results)