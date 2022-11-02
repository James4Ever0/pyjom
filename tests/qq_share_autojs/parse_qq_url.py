url = "mqqapi://share/to_fri?src_type=app&version=1&file_type=news&file_data=L3N0b3JhZ2UvZW11bGF0ZWQvMC9QaWN0dXJlcy9zaGFyZS8xMjcyMDY0MzU0&file_uri=Y29udGVudDovL3R2LmRhbm1ha3UuYmlsaS5maWxlcHJvdmlkZXIvb3BlbnNka19leHRlcm5hbC9zaGFyZTJxcV90ZW1wNDIwOTU0OTNhYjhlZGRhZmYzMWQ1Y2ZjYWYzZjE3MDQuanBn&title=5ZOU5ZOp5ZOU5ZOp&description=5aSn5Z6L5pS/6K6654mH772c5paw5pe25Luj562U5Y23&share_id=100951776&url=aHR0cHM6Ly9iMjMudHYvdGRKZGd6WT9zaGFyZV9tZWRpdW09YW5kcm9pZCZzaGFyZV9zb3VyY2U9cXEmYmJpZD1YWTFCQjcyMUIxRjk3MzQ4REJERTQyOTdGRTFCNEFCRTI2QkFBJnRzPTE2NjcyNzU0ODI4MTY=&app_name=5ZOU5ZOp5ZOU5ZOp&req_type=Nw==&mini_program_appid=MTEwOTkzNzU1Nw==&mini_program_path=cGFnZXMvdmlkZW8vdmlkZW8/YnZpZD1CVjFuZTQxMUw3aHkmc2hhcmVfc291cmNlPXFxX3VnYyZ1bmlxdWVfaz10ZEpkZ3pZ&mini_program_type=Mw==&cflag=MA==&third_sd=dHJ1ZQ=="

from urllib.parse import urlparse, parse_qs

parse_result=urlparse(url)
#print(parse_result)
#breakpoint()
#
#params=['count', 'encode', 'fragment', 'geturl', 'hostname', 'index', 'netloc', 'params', 'password', 'path', 'port', 'query', 'scheme', 'username']
#for k in params:
#    print("key:",k,"value:",eval("parse_result.{}".format(k)))

#[scheme]://[netloc/hostname]/[path]?[query]

dict_result=parse_qs(parse_result.query)

non_b64vals=["share_id","src_type","version","file_type"]

import base64
def dec_b64(v):
    if type(v) == str:
        v = v.encode()
    v=base64.b64decode(v)
    v=v.decode()
    return v


def enc_b64(v):
    if type(v) == str:
        v = v.encode()
    v=base64.b64encode(v)
    v=v.decode()
    return v

new_q={}
mypic="/storage/emulated/0/Pictures/share/cat.gif"
myuri='file://{}'.format(mypic)
shortlink="uHML5mi"
bvid="BV1zd4y117WF"
for k,v in dict_result.items():
    v=v[0]
    if k == "file_data":
        v=enc_b64(mypic)
    elif k == "file_uri":
        v=enc_b64(myuri)
    elif k == "share_id":
        v=100951776
    elif k == "url":
        v="https://b23.tv/"+shortlink
        v=enc_b64(v)
    elif k == "mini_program_path":
        v=enc_b64("pages/video/video?bvid="+bvid)
    elif k == "description":
        v=enc_b64("喵喵喵")
    new_q.update({k:v})
    #for printing purpose
    if k not in non_b64vals:
        v=dec_b64(v)
    print(k,":",v)
from urllib.parse import urlencode
new_qs=urlencode(new_q)
print()
template="am start -n com.tencent.mobileqq/com.tencent.mobileqq.activity.JumpActivity -a android.intent.action.VIEW -d 'mqqapi://share/to_fri?{}' -e pkg_name tv.danmaku.bili"
cmd=template.format(new_qs)
print(cmd)
import os
os.system(cmd)
