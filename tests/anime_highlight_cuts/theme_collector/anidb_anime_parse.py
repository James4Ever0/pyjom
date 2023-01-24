url = "https://anidb.net/anime/9310"


import requests
import fake_useragent
ua = fake_useragent.UserAgent()
r = requests.get(url, headers={"User-Agent":ua.random}) 

text = r.text
with open("")