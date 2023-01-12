#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/13 12:27
# @User    : zhunishengrikuaile
# @File    : 360config.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: me_blog

ROOT_URL = 'https://st.so.com/stu'  # 图片上传
NEXT_IMAGE_LIST = 'https://st.so.com/stu?a=simJson'  # 下一页sn=当前url返回值lastindex+1
CAICE_KEY_CONT = 'https://st.so.com/stu?a=BaikeJson&word='  # 获取到猜测的内容, 在猜测关键字存在的情况下返回
THIS_XIANGSHI_IMG = 'https://st.so.com/stu?a=siftwaterfalljson' # 获取到相识的图片

HEADERS = {
    'Host': 'st.so.com',
    'Content-Length': '359043',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Origin': 'https://st.so.com',
    'Upgrade-Insecure-Requests': '1',
    'enctype': "multipart/form-data",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://st.so.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Connection': 'keep-alive'
}
