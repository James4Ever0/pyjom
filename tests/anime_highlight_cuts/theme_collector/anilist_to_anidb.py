anilist_ids = [
    112788,  # 海边的异邦人
    14813,  # Yahari Ore no Seishun Love Come wa Machigatteiru.
]

# first let's get name.
from AnilistPython import Anilist

anilist = Anilist()

for anilist_id in anilist_ids:
    anime = anilist.get_anime_with_id(anilist_id)
    # what about alias?
    print(anime)
    print("=" * 20)
    romaji = anime.get("name_romaji", None)
    english = anime.get("name_english", None)
    # genres = anime.get("genres", []) # not so important. we don't have understanding.

    # and you will search again.
    # what is this manual select?
    # anime2 = anilist.get_anime(romaji) # shit?
    # print(anime2) # it will just be the same. no shit.
    # print("=" * 20)
    # well let's search in anidb. get different names.