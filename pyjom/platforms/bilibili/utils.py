import types
from bilibili_api import sync

# import json
from bs4 import BeautifulSoup
from lazero.utils.logger import sprint


# wtf is async generator type?
def bilibiliSync(func):
    def wrapper(*args, **kwargs):
        coroutineMaybe = func(*args, **kwargs)
        if type(coroutineMaybe) == types.CoroutineType:
            return sync(coroutineMaybe)
        else:
            return coroutineMaybe

    return wrapper


######## import all below functions to searchDataParser.
# from pyjom.platforms.bilibili.utils import generatorToList, linkFixer,traceError, extractLinks,videoDurationStringToSeconds,getAuthorKeywords,clearHtmlTags,splitTitleTags,removeAuthorRelatedTags


def generatorToList(generator):
    return [x for x in generator]


def linkFixer(link, prefix="http:"):
    if link.startswith("//"):
        return prefix + link
    return link


def traceError(errorMsg: str = "error!", _breakpoint: bool = False):
    import traceback

    traceback.print_exc()
    sprint(errorMsg)
    if _breakpoint:
        return breakpoint()


def extractLinks(description, extract_bgm=True):
    """Extract and remove links in description"""
    import re

    # notice, we don't need to go wild here. we just want the title and the cover, and the tags.
    expression = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    # expr = re.compile(expression)
    links = re.findall(expression, description)
    # if links == None:
    #     links = []
    desc_without_link = re.sub(expression, "", description)
    desc_without_link_per_line = [
        x.replace("\n", "").strip() for x in desc_without_link.split("\n")
    ]
    desc_without_link_per_line = [x for x in desc_without_link_per_line if len(x) > 0]
    bgms = []
    final_desc_list = []
    if not extract_bgm:
        final_desc_list = desc_without_link_per_line
    else:
        for line in desc_without_link_per_line:
            bgmCandidateTemplates = ["{}：", "{}:", "{} "]
            fixers = [x.format("") for x in bgmCandidateTemplates]
            bgmCandidates = [x.format("bgm") + "(.+)" for x in bgmCandidateTemplates]
            has_bgm = False
            for candidate in bgmCandidates:
                bgm_parse_result = re.findall(candidate, line.lower())
                if len(bgm_parse_result) > 0:
                    has_bgm = True
                    # bgm = line[len(bgmCandidates) :]
                    bgm = bgm_parse_result[0]
                    bgm = bgm.strip()
                    for fixer in fixers:
                        bgm = bgm.strip(fixer)
                    if len(bgm) > 0:
                        bgms.append(bgm)
                    break
            if not has_bgm:
                final_desc_list.append(line)
    desc_without_link = "\n".join(final_desc_list)
    return links, bgms, desc_without_link


from typing import Literal

import re

from typing import Union
def videoDurationStringToSeconds(
    durationString:Union[str, None], method: Literal["vtc", "basic"] = "vtc"
):
    if durationString in ["-", None]:
        return None
    if type(durationString) != str:
        return None
    if re.findall(r"\d", durationString) == []:
        return None
    try:
        if method == "vtc":
            import vtc

            timecode = "{}:0".format(durationString)
            decimal_seconds = vtc.Timecode(timecode, rate=1).seconds
            seconds = round(decimal_seconds)
            return seconds
        elif method == "basic":
            if type(durationString) == int:
                return durationString  # not string at all.
            if type(durationString) != str:
                print("unknown durationString type: %s" % type(durationString))
                return None
            durationString = durationString.strip()
            mList = durationString.split(":")[::-1]
            if len(mList) > 3:
                print("DURATION STRING TOO LONG")
                return None
            seconds = 0
            for index, elem in enumerate(mList):
                elem = int(elem)
                seconds += (60**index) * elem
            return seconds
        else:
            raise Exception("method %s does not exist" % method)
    except:
        import traceback

        traceback.print_exc()
        print("exception durion video duration string conversion")


def clearHtmlTags(htmlObject):
    a = BeautifulSoup(htmlObject, features="lxml")
    return a.text


def detectAuthorRelatedKeywords(title_tag, author_keywords):
    abandon = False
    for keyword in author_keywords:
        if len(keyword) > 1:
            if keyword in title_tag:
                abandon = True  # detected this thing.
                break
    return abandon


def getAuthorKeywords(author):
    author = author.strip()
    import jieba

    author_keywords = jieba.lcut(author)
    author_keywords = [x.strip() for x in author_keywords]
    author_keywords = [x for x in author_keywords if len(x) > 0]
    return author_keywords


def removeAuthorRelatedTags(description_or_title, author):
    templates = ["【{}】", "@{}", "{}"]
    tags = [template.format(author) for template in templates]
    for tag in tags:
        description_or_title = description_or_title.replace(tag, "")
    return description_or_title


def splitTitleTags(title, author_keywords):
    import re

    pattern = r"【.+】"
    title_tags = re.findall(pattern, title)
    title = re.sub(pattern, "", title)

    title_tags = [x.lstrip("【").rstrip("】").strip() for x in title_tags]
    title_tags = [x for x in title_tags if len(x) > 0]
    final_title_tags = []
    for title_tag in title_tags:
        detected = detectAuthorRelatedKeywords(title_tag, author_keywords)
        if not detected:
            final_title_tags.append(title_tag)
    return title, title_tags
