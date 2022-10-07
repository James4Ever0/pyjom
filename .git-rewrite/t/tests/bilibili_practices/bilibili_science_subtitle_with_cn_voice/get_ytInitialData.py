target = "curl_dump_youtube.html"

from bs4 import BeautifulSoup

# this is m.youtube.com/watch?v={videoId}
# import esprima
import js2py

soup = open(target,"r",encoding="utf-8").read()
soup = BeautifulSoup(soup,features="lxml")

scripts = soup.find_all("script")

jsfunc = lambda x: "function f9x() { "+x+ "  \n return ytInitialData;}"
jsfunc2 = lambda x: "function f9x() { "+x+ "  \n return ytInitialPlayerResponse;}"
# breakpoint()

from commons import *

data = None
data2 = None

for script in scripts:
    content = script.string
    if content is not None:
        if "var ytInitialPlayerResponse = {" in content:
            print("HAS DATA") # only one.
            # script_obj = esprima.parse(content)
            script_obj = jsfunc2(content)
            # print(script_obj)
            obj = js2py.eval_js(script_obj)
            # print(obj)
            data2 = obj() # need a json walker, from pyjom.
            # breakpoint()
    # print(content)
 

for script in scripts:
    content = script.string
    if content is not None:
        if "var ytInitialData = {" in content:
            print("HAS DATA") # only one.
            # script_obj = esprima.parse(content)
            script_obj = jsfunc(content)
            # print(script_obj)
            obj = js2py.eval_js(script_obj)
            # print(obj)
            data = obj() # need a json walker, from pyjom.
            # breakpoint()
    # print(content)
    # print("================================")

#     # breakpoint()

data_dict =  data.to_dict()
data2_dict =  data2.to_dict()
# print(type(data))
# breakpoint()

target1 = ["viewCountText","lengthText","publishedTimeText"]

targets = ["videoId", "simpleText"]

inits = ['contents', 'twoColumnWatchNextResults', 'secondaryResults', 'secondaryResults', 'results']
# inits2 = ['contents', 'twoColumnWatchNextResults', 'secondaryResults', 'secondaryResults', 'results']

ends2 = {"title":['compactVideoRenderer', 'title', 'simpleText'],"viewCountText": ['compactVideoRenderer', 'viewCountText', 'simpleText'],"publishTime":['compactVideoRenderer', 'publishedTimeText', 'simpleText'],"lengthText":['compactVideoRenderer', 'lengthText', 'simpleText'],"videoId":['compactVideoRenderer', 'videoId']}

videoDetails = data2_dict["videoDetails"]
videoDetails = {k:videoDetails[k] for k in ["viewCount","author","keywords","channelId","shortDescription","lengthSeconds","videoId","title"]}
# "https://i.ytimg.com/vi_webp/{videoId}/maxresdefault.webp # default cover.

videoDicts = {}
for key, content in json.walk(data_dict):
    # print(key)
    final_key = key[-1]
    if final_key in targets:
        if list_startswith(key,inits):
            for k in ends2.keys():
                v = ends2[k]
                if list_endswith(key,v):
                    valueType = k
                    value = content
                    valueIndex = key[len(inits)]
                    if valueIndex not in videoDicts.keys():
                        videoDicts[valueIndex] = {}
                    # print(valueIndex,valueType,value)
                    videoDicts[valueIndex].update({valueType:value})
                    break
        # print(key)  # i want to know the views of these.
    # breakpoint()

def getViewCount(vc): return vc.replace(",","").split(" ")[0]

def getLengthSeconds(lt):
    lt0 = lt.split(":")
    assert len(lt0) <=5 # no more than week please?
    dicIndex = {0:1,1:60,2:60*60,3:60*60*24,4:60*60*24*7}
    seconds = 0
    for i,v in enumerate(reversed(lt0)):
        vn = int(v)
        vs = vn*dicIndex[i]
        seconds += vs
    return str(seconds)

for k in videoDicts.keys():
    v = videoDicts[k]
    viewCount = getViewCount(v["viewCountText"])
    v.update({"viewCount":viewCount})
    lengthSeconds = getLengthSeconds(v["lengthText"])
    v.update({"lengthSeconds":lengthSeconds})
    print(v)
    # for k0 in ends2.keys():
    #     assert k0 in v.keys()

print(videoDetails)