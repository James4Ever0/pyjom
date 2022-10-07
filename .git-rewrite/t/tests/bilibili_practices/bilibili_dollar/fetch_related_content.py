#!pip3 install youtube-search-python

from youtubesearchpython import VideosSearch

# videosSearch = VideosSearch('画人民币', limit = 10)
videosSearch = VideosSearch('Draw realistic US Dollar', limit = 10)
# videosSearch = VideosSearch('NoCopyrightSounds', limit = 2)

# print(videosSearch.result())
data = videosSearch.result()
for elem in data["result"]:
    title = elem["title"]
    videoId = elem["id"]
    contentType = elem["type"]
    authorName = elem["channel"]["name"]
    channelId = elem["channel"]["id"]
    viewCount = elem["viewCount"]["text"]
    print("title",title)
    print("videoId",videoId)
    print("author",authorName)
    print("channel ID",channelId)
    print("viewCount",viewCount)
    print("_______________________________________")
