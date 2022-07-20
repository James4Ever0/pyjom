source = "sample.html"

# curl -L -o sample.html "https://anime1.me/category/2022%e5%b9%b4%e6%98%a5%e5%ad%a3/%e5%8b%87%e8%80%85%e8%be%ad%e8%81%b7%e4%b8%8d%e5%b9%b9%e4%ba%86"

from bs4 import BeautifulSoup

data = open(source,"r",encoding="utf-8").read()
dom = BeautifulSoup(data)
# dom = BeautifulSoup(data,features='lxml')
import urllib.parse as up
import json
import re
videos = dom.find_all("video")

format_download_link = lambda c,e: "https://shiro.v.anime1.me/{}/{}.mp4".format(c,e)

for video in videos:
    # print(dir(video))
    data_src = "data-apireq"
    json_obj = video[data_src]
    json_obj = up.unquote(json_obj)
    json_obj = json.loads(json_obj)
    channel, episode = json_obj["c"], json_obj["e"]
    link = format_download_link(channel, episode)
    episode_id = re.findall(r"\d+",episode)[0]
    print("EPISODE:",episode_id)
    print("DOWNLOAD LINK:",link)
    # breakpoint()