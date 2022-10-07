download_path = "exciting_bgm.mp3" # is the extension right?

import requests
baseUrl = "http://localhost:4000"

keyword = "last friday night" # american pop music?

search_result = requests.get(baseUrl+"/cloudsearch", params={"keyword": keyword})

print(search_result.content)
breakpoint()