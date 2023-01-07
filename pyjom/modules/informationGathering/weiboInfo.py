from pyjom.commons import *
import requests
import random
import jieba
import json
import parse
import urllib.parse


def weiboLinkSearch(keyword):
    links = []
    myfilter = list(jieba.cut(keyword))
    myfilter = [x for x in myfilter if chineseDetector(x)]
    page = random.randint(
        1, 100
    )  # just a demo we do not know how to handle this one just yet.
    url = sinaWeiboApi["search_with_page"].format(keyword, page)
    with requests.get(url) as r:
        print("STATUS_CODE:", r.status_code)
        if r.status_code == 200:
            content = r.content.decode("utf-8")
            content = parse.parse("initFeed({content})", content)
            content = content["content"]
            # import pyperclip
            # pyperclip.copy(content)
            # print(content)
            content = json.loads(content)
            data = content["data"]
            feed1 = data["feed1"]
            for elem in feed1:
                url = elem["url"]
                title = elem["title"]
                fsum = 0
                for f in myfilter:
                    if f in title:
                        fsum += 1
                if fsum == len(myfilter):
                    links.append(url)
            return links


def weiboStatusParser(content):
    mtitle = None
    if "topic_struct" in content.keys():
        mtopic = [(x["topic_title"], x["topic_url"]) for x in content["topic_struct"]]
    else:
        mtopic = None
    mtext_raw = content["text_raw"]
    mtext = content["text"]
    mtime = content["created_at"]
    mauthor = content["user"]["screen_name"]
    mid = content["idstr"]  # used for fetching comments.
    mauthor_id = content["user"]["idstr"]
    mblogid = content["mblogid"]
    reposts_count = content["reposts_count"]
    comments_count = content["comments_count"]
    attitudes_count = content["attitudes_count"]
    mfeedback = {
        "reposts_count": reposts_count,
        "comments_count": comments_count,
        "attitudes_count": attitudes_count,
    }

    mcontent = {
        "video": None,
        "picture": None,
        "title": mtitle,
        "topic": mtopic,
        "text": {"raw": mtext_raw, "html": mtext},
        "author": mauthor,
        "meta": {"time": mtime, "id": mid, "mblogid": mblogid, "uid": mauthor_id},
        "feedback": mfeedback,
    }
    if len(content["pic_ids"]) > 0 and content["pic_num"] > 0:
        print("picture count:", content["pic_num"])
        content["picture"] = []
        for pid in content["pic_ids"]:
            pic_srcs = [
                "original",
                "mw2000",
                "largest",
                "large",
                "bmiddle",
                "thumbnail",
            ]
            picBase = content["pic_infos"][pid]
            picUrl = None
            for src in pic_srcs:
                if src in picBase.keys():
                    picUrl = picBase[src]
                    if "url" in picUrl.keys():
                        picUrl = picUrl["url"]
                        if picUrl is not None:
                            print("fetched picture [{}]\n{}".format(src, picUrl))
                            break
            if picUrl is not None:
                content["picture"].append(picUrl)
            # only select the clearest, if possible.
    elif "page_info" in content.keys():
        print(content["page_info"])  # this is how you print it.
        videoBase = content["page_info"]["media_info"]
        potential_links = [
            "stream_url_hd",
            "mp4_hd_url",
            "h265_mp4_hd",
            "inch_4_mp4_hd",
            "inch_5_mp4_hd",
            "inch_5_5_mp4_hd",
            "mp4_sd_url",
            "stream_url",
            "h265_mp4_ld",
            "mp4_720p_mp4",
            "hevc_mp4_720p",
        ]
        h5_url = videoBase["h5_url"]
        download_link = [videoBase[x] for x in potential_links if videoBase[x] != ""][0]
        mvideo_info = {
            "video_orientation": videoBase["video_orientation"],
            "h5_url": h5_url,
            "download_link": download_link,
        }
        mcontent["video"] = mvideo_info
        # print(list(videoBase.keys()))
        if "video_title" not in videoBase.keys():
            try:
                mcontent["title"] = videoBase["titles"][0]["title"]
            except:
                try:
                    mcontent["title"] = videoBase["content2"]
                except:
                    try:
                        mcontent["title"] = videoBase["video_title"]
                    except:
                        try:
                            mcontent["title"] = videoBase["next_title"]
                        except:
                            try:
                                mcontent["title"] = videoBase["cards"][0]["content2"]
                            except:
                                mcontent["title"] = videoBase["page_title"]
        else:
            mcontent["title"] = videoBase["video_title"]
    return mcontent


def weiboVideoSearch(keyword):
    links = weiboLinkSearch(keyword)
    # info = []
    for link in links:  # use yleid here.
        myId = link.split("/")[-1]
        # need cookie to do the job?
        videoLink = sinaWeiboApi["weibo_status_by_blogid"].format(
            myId
        )  # sina got better grammar?
        # videoLink = "https://www.weibo.com/ajax/status/show?id="+myId
        with requests.get(videoLink) as r:
            print("fetching video link:", videoLink)
            print("STATUS_CODE:", r.status_code)
            if r.status_code == 200:
                content = r.text
                # print('response content:',content)
                # this is not formatted. this is pure json i suppose.
                # content = parse.parse("initFeed({content})",content)
                if content == None:
                    print("skipping link:", videoLink)
                    continue
                # content = content["content"]
                # with open("{}.json".format(myId),"w+",encoding="utf-8") as f:
                #     f.write(content)
                content = json.loads(content)
                mcontent = weiboStatusParser(content)  # this is a generator, not a list.
                yield mcontent # this is a generator, not a list. how to get our feedback?
        # return info
        # make it into generator so links will not expire so damn fast.


def weiboInfoLogic(topic):
    infoDict = {}
    for elem in topic["entities"]:
        keyword = elem["chinese"]
        if keyword is not None:
            info = weiboVideoSearch(keyword)
            infoDict.update({keyword: info})
    return infoDict


@decorator
def weiboInfo(topic):
    infoDict = weiboInfoLogic(topic)
    return infoDict


@decorator
def weiboFetcher(topic):
    mtopic_bytes = json.dumps(topic).encode()
    protocol = "sinafetch://{}".format(
        urllib.parse.quote(mtopic_bytes)
    )  # this is the posted_location, submit to feedback. containing the keyword in json.
    # which is not desired since in this way we will not get the feedback.
    infoDict = weiboInfoLogic(topic)
    return protocol, infoDict
