anilist_id = 112788

# first let's get name.
from AnilistPython import Anilist
anilist = Anilist()
anime = anilist.get_anime_with_id(anilist_id)
# what about name>