#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/13 12:29
# @User    : zhunishengrikuaile
# @File    : main.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: me_blog
import requests
from urllib import parse
from bs4 import BeautifulSoup
from config360 import ROOT_URL, NEXT_IMAGE_LIST, CAICE_KEY_CONT, HEADERS, THIS_XIANGSHI_IMG


class SearchImage360(object):
    def __init__(self, image=None, imageurl=None):
        '''
        upload
        imgurl	https://p3.ssl.qhimgs1.com/sdr/_142_/t01f9533f2c6045c0c3.jpg
        base64image
        submittype	imgurl
        src	st
        srcsp	st_search
        cut
        imgkey	t0177307fc503acee35.jpg
        :param image:
        '''
        self.image = image
        self.imageurl = imageurl
        if image:
            self.multiple_files = [
                ('upload', ('foo.png', open(self.image, 'rb'), 'image/png'))]

        if imageurl:
            self.multiple_data = {
                'upload': '',
                'imgurl': self.imageurl,
                'base64image': '',
                'submittype': 'imgurl',
                'src': 'st',
                'srcsp': 'st_search',
                'cut': '',
            }

    def upload(self):
        if self.imageurl:
            url_post = requests.post(url=ROOT_URL, data=self.multiple_data, headers=HEADERS)
        else:
            url_post = requests.post(url=ROOT_URL, files=self.multiple_files, headers=HEADERS)

        url_str = str(url_post.url)  # 获取到url参数
        params = parse.parse_qs(parse.urlparse(url_str).query)
        print("PARAMS?",params)
        url_str = params['imgkey'][0]
        # 获取图片猜测
        buf_sellect = BeautifulSoup(url_post.text, 'html5lib')
        wd_select = buf_sellect.select('#search_kw')
        for x in wd_select:
            keywd = x.get('value')
        return {'keywd': keywd, 'url_str': url_str}

    @classmethod
    def thisnextpage(cls, url_key, sn=0, pn=30):
        page_url = NEXT_IMAGE_LIST + '&imgkey={KEY}&sn={SN}&pn={PN}&cut=0'.format(KEY=url_key, SN=sn, PN=pn)
        result = requests.get(url=page_url, verify=False)
        return result.json()

    @classmethod
    def caiceinfo(cls, wdkey):
        info_url = CAICE_KEY_CONT + wdkey
        result = requests.get(url=info_url, verify=False)
        return result.json()

    @classmethod
    def xiangshiimg(cls, url_key, sn=0, pn=30):
        xiangshiimg_url = THIS_XIANGSHI_IMG + '&imgkey={URL_KEY}&cut=0&sn={SN}&pn={PN}'.format(URL_KEY=url_key, SN=sn,
                                                                                               PN=pn)
        print(xiangshiimg_url)
        result = requests.get(url=xiangshiimg_url, verify=False)
        return result.json()


if __name__ == '__main__':
    set = SearchImage360(image='testimg/dm.jpeg',
                         imageurl=None)
    # 'https://p0.ssl.qhimgs1.com/sdr/_142_/t01c3d15be40763a850.jpg'
    wdkey_urlkey = set.upload()
    keywd = wdkey_urlkey.get('keywd')
    url_str = wdkey_urlkey.get('url_str')
    print(wdkey_urlkey)

    # 获取相识的图片
    if url_str != '':
        this_page_cont = set.thisnextpage(url_key=url_str)
        print('相识：', this_page_cont)

    # 获取百科图片
    if keywd != '':
        ciace = set.caiceinfo(keywd)
        print('百科,', ciace)

    # 获取相同图片
    xiangshi = set.xiangshiimg(url_key=url_str)
    print('相同:', xiangshi)
