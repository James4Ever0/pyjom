download_path = "exciting_bgm.mp3" # is the extension right?

import requests
baseUrl = "http://localhost:4000"

keywords = "last friday night" # american pop music?

search_result = requests.get(baseUrl+"/cloudsearch", params={"keywords": keywords})

print(search_result.json())
breakpoint()