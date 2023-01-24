# anilist has typo on "Yahari Ore no Seishun Lovecome wa Machigatte Iru." which might be harmful.
imagePath = ""
import requests
data =requests.post("https://api.trace.moe/search",
  data=open(imagePath, "rb"), # since this is smallest
  headers={"Content-Type": "image/jpeg"}
).json()

import rich
rich.print(data)
breakpoint()