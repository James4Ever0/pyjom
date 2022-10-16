get_download_path = lambda extension:"exciting_bgm.{}".format(extension) # is the extension right?

import requests
baseUrl = "http://localhost:4000"
# now what is the port?
# 4042

keywords = "last friday night" # american pop music?
import time

def getJSTimeStamp(): return int(time.time()*1000)

# {'data': {'code': 200, 'account': {'id': 7935782775, 'userName': '0_fxg_pxw@163.com', 'type': 0, 'status': -10, 'whitelistAuthority': 0, 'createTime': 1657240405751, 'tokenVersion': 0, 'ban': 0, 'baoyueVersion': 0, 'donateVersion': 0, 'vipType': 0, 'anonimousUser': False, 'paidFee': False}, 'profile': None}}
# breakpoint()
# phone, password = "19825089619","dbH361210110"
# login_response = requests.get(baseUrl+"/login/cellphone",params={"phone": phone,"password": password})
# login_response = requests.get(baseUrl+"/logout")
# login_response_json = login_response.json()
# print(login_response_json)

# login_response = requests.get(baseUrl+"/register/anonimous")
# login_response_json = login_response.json()
# # {'code': -460, 'message': '网络太拥挤，请稍候再试！'}
# # what the fuck is this shit?
# print(login_response_json)


# login_status = requests.get(baseUrl+"/login/status")
# login_status_json = login_status.json()
# print(login_status_json)

# breakpoint()

search_result = requests.get(baseUrl+"/search", params={"keywords": keywords, "timestamp":getJSTimeStamp()})
# search_result = requests.get(baseUrl+"/cloudsearch", params={"keywords": keywords, "timestamp":getJSTimeStamp()})

search_result_json = search_result.json() # check search_result.json
# breakpoint()
code = search_result_json["code"]
# print(search_result_json)
# breakpoint()
# {'msg': '操作频繁，请稍候再试', 'code': 405, 'message': '操作频繁，请稍候再试'} # too frequent.


if not code == 200:
    print("ERROR CODE IN SEARCH:", code)
    print(search_result_json)
else:# no error here.
    result = search_result_json["result"]
    songs = result["songs"]
    mySong = songs[1]
    mySongName = mySong["name"]
    mySongId = mySong["id"]
    if "ar" in mySong.keys():
        mySongArtists = mySong["ar"] # reserved for further use. like find other songs by the artist.
    elif "artists" in mySong.keys():
        mySongArtists = mySong["artists"]
    else: mySongArtists = []
    # mySong["artists"]

    print("SELECTED SONG:")
    print(mySongName, mySongId, mySongArtists)

    # download that thing.
    download_result = requests.get(baseUrl + "/song/url", params = {"id":mySongId}) # 试听歌曲
    # download_result = requests.get(baseUrl + "/song/url", params = {"id":mySongId, "timestamp":getJSTimeStamp()}) # 试听歌曲
    download_result_json = download_result.json()

    print(download_result_json) # no download url!
    # breakpoint()
    code = download_result_json["code"]
    if code == 200: # allow to download now?
        myDownloads = download_result_json["data"]
        myDownload = myDownloads[0]
        myDownloadUrl = myDownload["url"]
        myDownloadType = myDownload["type"]

        # now download the thing.
        result = requests.get(myDownloadUrl) # no need for timestamp?
        if result.status_code == 200:
            data = result.content
            with open(get_download_path(myDownloadType),"wb") as f:
                f.write(data)
            print("DOWNLOAD SONG DONE.") # you should check the duration of this music file.
            # 2871154
            lyrics_result = requests.get("http://localhost:4000/lyric",{"id":mySongId, "timestamp":getJSTimeStamp()})
            # this is cached.
            lyrics_result_json = lyrics_result.json()
            if lyrics_result_json["code"] == 200:
                lrc = lyrics_result_json["lrc"]
                if type(lrc) == dict:
                    version = lrc["version"]
                    lyric = lrc["lyric"]
                    if type(lyric) == str:
                        with open(
                            "exciting_bgm.lrc","w") as f0: f0.write(lyric)
                        print("LYRIC DOWNLOAD DONE.")
            # THIS IS FREAKING WRONG... SHALL I LOGIN?
            # Duration                                 : 30 s 41 ms