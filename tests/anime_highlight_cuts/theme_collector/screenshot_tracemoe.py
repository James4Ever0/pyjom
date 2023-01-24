# anilist has typo on "Yahari Ore no Seishun Lovecome wa Machigatte Iru." which might be harmful.
imagePath = "/Users/jamesbrown/Downloads/gay_anime_shot.jpeg"
import requests
data =requests.post("https://api.trace.moe/search",
  data=open(imagePath, "rb"), # since this is smallest
  headers={"Content-Type": "image/jpeg"}
).json() # remember you must change your ip later.

import rich
rich.print(data) # the anime character recognition website is not running so well.
# breakpoint()
error = data['error']
assert error == ""

results = data['result']

for result in results: # already sorted.
    anilist_id = result['anilist']
    filename = result['filename'] # need parsing right?
    episode = result.get('episode', None)
    start, end = result['from'], result['end']
    similarity = result['similarity']