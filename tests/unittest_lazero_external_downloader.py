from lazero.network.downloader import download

url = "https://media3.giphy.com/media/wTrXRamYhQzsY/giphy.gif?cid=dda24d502m79hkss38jzsxteewhs4e3ocd3iqext2285a3cq&rid=giphy.gif&ct=g"

path = "/dev/shm/medialang/test.gif"

import os

if os.path.exists(path):
    os.remove(path)

report = download(url, path)

print("download success?", report)
