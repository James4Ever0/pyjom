download_path = "exciting_bgm.mp3" # is the extension right?

import requests
baseUrl = "http://localhost:4000"

keywords = "last friday night" # american pop music?

search_result = requests.get(baseUrl+"/cloudsearch", params={"keywords": keywords})

search_result_json = search_result.json() # check search_result.json
# breakpoint()
code = search_result_json["code"]
result = search_result_json["result"]

if code == 200: # no error here.
    songs = result["songs"]
    mySong = songs[0]
    mySongName = mySong["name"]
    mySongId = mySong["id"]
    mySongArtists = mySong["ar"] # reserved for further use. like find other songs by the artist.

    print("SELECTED SONG:")
    print(mySongName, mySongId, mySongArtists)

    # download that thing.
    download_result = requests.get(baseUrl + "/song/download/url", params = {"id":mySongId})
    download_result_json = download_result.json()

    print(download_result_json)
    breakpoint()