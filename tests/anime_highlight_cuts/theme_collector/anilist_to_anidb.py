anilist_ids = [112788, #海边的yi bang ren
]

# first let's get name.
from AnilistPython import Anilist
anilist = Anilist()

for anilist_id in anilist_ids:
    anime = anilist.get_anime_with_id(anilist_id)
    # what about alias?