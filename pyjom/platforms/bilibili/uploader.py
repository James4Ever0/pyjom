from bilibili_api import video_uploader, Credential
from pyjom.platforms.bilibili.credentials import bilibiliCredential
import os

from pyjom.platforms.bilibili.utils import bilibiliSync

# you may use the 'sync' method elsewhere.
# damn. out of sync.
# recall the order of applying decorators
# WTF is the order?


@bilibiliSync
async def asyncVideoUploader(
    videoPath, title, description, meta, credential, cover_path
):
    page = video_uploader.VideoUploaderPage(
        path=videoPath,
        title=title,
        description=description,
    )  # are you sure?
    uploader = video_uploader.VideoUploader(
        [page], meta, credential, cover_path=cover_path
    )

    # will this work as expected?
    # @uploader.on("__ALL__")
    # async def ev(data):
    #     print(data)

    result = await uploader.start()  # with bvid, aid as key.
    # please tell me where the fuck you upload my video upto?
    # print("upload video result:", result)
    return result # there's no upload_id. but you can do it in other way, with methods inside the class.
    # if possible please return something like upload_id?
    # upload video result: {'aid': 901508571, 'bvid': 'BV1MN4y1P7mq'}
    # breakpoint()  # comment it out later? or we will check why this upload fails. maybe it is because we have duplicated name/cover.
    # return result["bvid"]  # choose to be in this way?


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import math
import base64
import requests
from requests.adapters import HTTPAdapter
import threading
from threading import Event
import copy
import traceback


# you better embed it inside your function? what a creep?
# but that will make it impossible to test against other shits.
class MultithreadUploader(object):
    ## what is the cookie string look like?
    def __init__(self, cookie_string):
        # TODO: 增加登录接口使用账号密码登陆
        #  get all related shits?
        cookie = cookie_string
        self.MAX_RETRYS = 5
        self.profile = "ugcupos/yb"
        self.cdn = "ws"
        self.csrf = re.search("bili_jct=(.*?);", cookie + ";").group(1)
        self.mid = re.search("DedeUserID=(.*?);", cookie + ";").group(1)
        self.session = requests.session()
        self.session.mount("https://", HTTPAdapter(max_retries=self.MAX_RETRYS))
        self.session.headers["cookie"] = cookie
        self.session.headers[
            "Accept"
        ] = "application/json, text/javascript, */*; q=0.01"
        self.session.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        self.session.headers["Referer"] = "https://space.bilibili.com/{mid}/#!/".format(
            mid=self.mid
        )
        self.upload_id = None

    def _preupload(self, filename, filesize):

        # 1.获取本次上传所需信息
        preupload_url = "https://member.bilibili.com/preupload"
        params = {
            "os": "upos",
            "r": "upos",
            "ssl": "0",
            "name": filename,
            "size": filesize,
            "upcdn": self.cdn,
            "profile": self.profile,
        }
        response = self.session.get(preupload_url, params=params)
        upload_info = response.json()

        # 本次上传bilibili端文件名
        upload_info["bili_filename"] = (
            upload_info["upos_uri"].split("/")[-1].split(".")[0]
        )
        # 本次上传url
        endpoint = "http:%s/" % upload_info["endpoint"]
        upload_url = re.sub(r"^upos://", endpoint, upload_info["upos_uri"])
        print("UPLOAD URL:", upload_url, file=sys.stderr)
        # 本次上传session
        upload_session = requests.session()
        upload_session.mount("http://", HTTPAdapter(max_retries=self.MAX_RETRYS))
        upload_session.headers["X-Upos-Auth"] = upload_info["auth"]

        # 2.获取本次上传的upload_id
        response = upload_session.post(upload_url + "?uploads&output=json")
        upload_info["upload_id"] = response.json()[
            "upload_id"
        ]  # here you have upload_id
        self.upload_id = upload_info["upload_id"]

        print("UPLOAD INFO:", upload_info, file=sys.stderr)
        return upload_url, upload_info, upload_session

    def _multithread_upload(
        self, filepath, filesize, upload_url, upload_info, upload_session
    ):
        # 3.分块上传文件
        CHUNK_SIZE = 4 * 1024 * 1024
        total_chunks = math.ceil(filesize * 1.0 / CHUNK_SIZE)
        offset = 0
        chunk = 0
        parts_info = {"parts": []}
        with open(filepath, "rb") as fp:
            events = []
            while True:
                blob = fp.read(CHUNK_SIZE)
                if not blob:
                    break
                params = {
                    "partNumber": chunk + 1,
                    "uploadId": upload_info["upload_id"],
                    "chunk": chunk,
                    "chunks": total_chunks,
                    "size": len(blob),
                    "start": offset,
                    "end": offset + len(blob),
                    "total": filesize,
                }
                # here we go?
                def multiparts():
                    blob0 = copy.deepcopy(blob)
                    chunk0 = chunk
                    thisevent = Event()
                    events.append(thisevent)
                    offset0 = offset
                    while True:
                        try:
                            response = upload_session.put(
                                upload_url, params=params, data=blob0
                            )
                            print(
                                "Uploading...",
                                math.floor(chunk0 / total_chunks * 100),
                                "%  UPLOAD CHUNK",
                                chunk0,
                                ":",
                                response.text,
                                file=sys.stderr,
                            )
                            print("done for {}".format(offset0))
                            thisevent.set()
                            break
                        except:
                            print("error in chunk {}".format(offset0))
                            traceback.print_exc()

                threading.Thread(target=multiparts, args=(), daemon=True).start()

                parts_info["parts"].append({"partNumber": chunk + 1, "eTag": "etag"})
                chunk += 1
                offset += len(blob)
            for event in events:
                event.wait()
            print("finished waiting.")
        return parts_info

    def _upload(self, filepath):
        """执行上传文件操作"""
        if not os.path.isfile(filepath):
            print("FILE NOT EXISTS:", filepath, file=sys.stderr)
            return

        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        upload_url, upload_info, upload_session = self._preupload(filename, filesize)
        # 4.标记本次上传完成
        parts_info = self._multithread_upload(
            filepath, filesize, upload_url, upload_info, upload_session
        )
        params = {
            "output": "json",
            "name": filename,
            "profile": self.profile,
            "uploadId": upload_info["upload_id"],
            "biz_id": upload_info["biz_id"],
        }
        response = upload_session.post(upload_url, params=params, data=parts_info)
        print(
            "UPLOAD RESULT:",
            response.text,
            file=sys.stderr,  # but till then we can use the upload_id.
        )  # here we do not have the result.

        return upload_info  # still, not the bvid thing we want.

    def _cover_up(self, image_path):
        """上传图片并获取图片链接"""
        if not os.path.isfile(image_path):
            return ""
        import tempfile
        import cv2

        with tempfile.NamedTemporaryFile(suffix=".jpg") as f:
            jpeg_image_path = f.name
            image = cv2.imread(image_path)
            cv2.imwrite(jpeg_image_path, image)
            fp = open(jpeg_image_path, "rb")
            encode_data = base64.b64encode(fp.read())
            # warning. forced to use jpeg.
            url = "https://member.bilibili.com/x/vu/web/cover/up"
            data = {
                "cover": b"data:image/jpeg;base64," + encode_data,
                "csrf": self.csrf,
            }
            response = self.session.post(url, data=data)
            return response.json()["data"]["url"]

    def upload_video_and_cover(self, filepath, cover_path):
        # 上传文件, 获取上传信息
        upload_info = self._upload(filepath)
        if not upload_info:
            ## fuck?
            print("upload failed?")
            return {}, ""
        # 获取图片链接
        cover_url = self._cover_up(cover_path) if cover_path else ""
        return upload_info, ""

    def postupload(self, upload_info, cover_url, metadata):

        title = ""
        tid = 0
        tag = ""
        desc = ""
        source = ""
        # cover_path="",
        dynamic = ""
        # mission_id = None
        no_reprint = 1
        """视频投稿
        Args:
            filepath   : 视频文件路径
            title      : 投稿标题
            tid        : 投稿频道id,详见https://member.bilibili.com/x/web/archive/pre
            tag        : 视频标签，多标签使用','号分隔
            desc       : 视频描述信息
            source     : 转载视频出处url
            cover_path : 封面图片路径
            dynamic    : 分享动态, 比如："#周五##放假# 劳资明天不上班"
            no_reprint : 1表示不允许转载,0表示允许
        """
        # TODO:
        # 1.增加多P上传
        # 2.对已投稿视频进行删改, 包括删除投稿，修改信息，加P删P等

        # 设置视频基本信息
        params = {
            "source": source,
            "title": title,
            "tid": tid,
            "tag": tag,
            "no_reprint": no_reprint,
            "desc": desc,
            # "mission_id": mission_id,
            "desc_format_id": 0,
            "dynamic": dynamic,
            "cover": cover_url,
            "videos": [
                {
                    "filename": upload_info["bili_filename"],
                    "title": title,
                    "desc": "",
                }
            ],
        }
        params.update(metadata)
        # 版权判断, 转载无版权
        params["copyright"] = 2 if params.get("source") else 1
        if source:
            del params["no_reprint"]
        # tag设置
        mtag = params.get("tag")
        if isinstance(mtag, list):
            params["tag"] = ",".join(mtag)
        # if mission_id is None:
        #     del params["mission_id"]
        url = "https://member.bilibili.com/x/vu/web/add?csrf=" + self.csrf
        response = self.session.post(url, json=params)
        print("SET VIDEO INFO:", response.text, file=sys.stderr)
        return response.json() # {"code":0,"message":"0","ttl":1,"data":{"aid":604946025,"bvid":"BV1y84y1v7tM"}}
        # seriously, it is a ugc platform.
        ## what is this fucking json?

    def upload(
        self,
        filepath: str,
        cover_path: str,
        metadata: dict,
    ):
        upload_info, cover_url = self.upload_video_and_cover(filepath, cover_path)
        if upload_info == {}:
            # something went wrong.
            return
        response_json = self.postupload(upload_info, cover_url, metadata)
        return response_json


def getCookieStringFromCookieDict(cookies_dict, mustcook=["DedeUserID", "bili_jct"]):
    cookies = cookies_dict
    cookie_string = ""
    for x in mustcook:
        assert x in cookies.keys()
    # ckeys = mustcook + [x for x in cookies.keys() if x not in mustcook]
    # assert "bili_jct" in cookies.keys()
    for key in mustcook:
        assert key in cookies.keys()
    # breakpoint()
    for key, value in cookies.items():  # oh shit maybe i know it.
        if key is not None and value is not None:
            cookie_string += key + "=" + value + "; "
    cookie_string = cookie_string[:-2]
    return cookie_string

##############################################################
def videoMultithreadUploader(
    cookies_dict: dict = ...,
    filepath: str = ...,
    coverpath: str = ...,
    metadata: dict = ...,
):

    # append new events?
    # planning using two jsons. one for credential, one for video details.
    # get picture.
    cookie_string = getCookieStringFromCookieDict(cookies_dict)
    # while True:
    try:
        uper = MultithreadUploader(cookie_string)
        data = uper.upload(filepath, coverpath, metadata)
        return True, data
    except:
        print("Exception found when uploading video.")
        traceback.print_exc()
        return False, {}


##############################################################

# @bilibiliSync
# no need to be sync. really?
@bilibiliCredential  # keyword 'dedeuserid' with default value.
def uploadVideo(
    credential: Credential = ...,
    # sessdata="",
    # bili_jct="",
    # buvid3="", # credentials.
    # dedeuserid: str = "397424026",
    description: str = "",
    dynamic: str = "",
    tagString: str = "",
    tagId: int = 21,  # what is 21? -> 日常
    title: str = "",
    close_danmaku: bool = False,
    close_reply: bool = False,
    videoPath: str = "",
    cover_path: str = "",
    multithread: bool = True,
    # threads=3,
):
    # title='abdefg'
    assert os.path.exists(videoPath)
    assert os.path.exists(cover_path)
    cookie_dict = {
        key: credential.__dict__[key.lower()]
        for key in ["buvid3", "DedeUserID", "bili_jct", "SESSDATA"]
    }
    # videoExtension = videoPath.split(".")[-1].lower()
    # credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3)
    # you can pass it from somewhere else.
    # 具体请查阅相关文档
    meta = {
        "copyright": 1,
        "source": "",  # no source?
        "desc": description,
        "desc_format_id": 0,
        "dynamic": dynamic,  # could be the same as desc.
        "interactive": 0,
        "open_elec": 1,
        "no_reprint": 1,
        "subtitles": {"lan": "", "open": 0},
        "tag": tagString,
        "tid": tagId,  # original is 21. what is it?
        "title": title,
        "up_close_danmaku": close_danmaku,
        "up_close_reply": close_reply,
    }
    if multithread:
        no_exception, mresult = videoMultithreadUploader(cookie_dict, videoPath, cover_path, meta)
        if not no_exception:
            raise Exception('videoMultithreadUploader error')
        try:
            code, message = mresult.get('code'), mresult.get('message')
            assert code == 0  # 为什么分区暂时不可用？
            assert message == '0'
        except:
            print("Uploading to bilibili failed")
            breakpoint()
            print()
            raise Exception('videoMultithreadUploader error: invalid response:', mresult)
        result = mresult.get('data',{})
    else:
        result = asyncVideoUploader(
            videoPath, title, description, meta, credential, cover_path
        )
    print("multithread?", multithread)
    print("upload video result:", result)
    try:
        assert 'aid' in result.keys()
        assert 'bvid' in result.keys()
    except:
        raise Exception("error: no valid upload result obtained:", result)
        # {'aid': 817422346, 'bvid': 'BV1NG4y1t7zk'}
        # in this format.
    return result


# host your web application online, then make money through it!
