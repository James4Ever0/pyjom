get_download_path = lambda extension:"exciting_bgm.{}".format(extension) # is the extension right?

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
    download_result = requests.get(baseUrl + "/song/url", params = {"id":mySongId}) # 试听歌曲
    download_result_json = download_result.json()

    # print(download_result_json) # no download url!
    # breakpoint()
    code = download_result_json["code"]
    if code == 200: # allow to download now?
        myDownloads = download_result_json["data"]
        myDownload = myDownloads[0]
        myDownloadUrl = myDownload["url"]
        myDownloadType = myDownload["type"]

        # now download the thing.
        result = requests.get(myDownloadUrl)
        if result.status_code == 200:
            data = result.content
            with open(get_download_path(myDownloadType),"wb") as f:
                f.write(data)
            print("DOWNLOAD SONG DONE.")
            # THIS IS FREAKING WRONG... SHALL I LOGIN?
            # Duration                                 : 30 s 41 ms