anilist_ids = [112788, #海边的异邦人
14813 #Yahari Ore no Seishun Love Come wa Machigatteiru.
]

# first let's get name.
from AnilistPython import Anilist
anilist = Anilist()

for anilist_id in anilist_ids:
    anime = anilist.get_anime_with_id(anilist_id)
    # what about alias?
    print(anime)
    print("=====================")