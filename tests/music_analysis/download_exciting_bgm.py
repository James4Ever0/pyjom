get_download_path = lambda extension:"exciting_bgm.{}".format(extension) # is the extension right?

import requests
baseUrl = "http://localhost:4000"

keywords = "last friday night" # american pop music?

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
    download_result = requests.get(baseUrl + "/song/download/url", params = {"id":mySongId}) # 试听歌曲
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
        result = requests.get(myDownloadUrl)
        if result.status_code == 200:
            data = result.content
            with open(get_download_path(myDownloadType),"wb") as f:
                f.write(data)
            print("DOWNLOAD SONG DONE.")
            # THIS IS FREAKING WRONG... SHALL I LOGIN?
            # Duration                                 : 30 s 41 ms