from pyjom.commons import *
import requests
import json


def weiboCheckFeedback(meta, with_user=False):
    feedback = {"comments": []}
    id_ = meta["id"]
    uid = meta["uid"]
    url = sinaWeiboApi["weibo_build_comments"].format(100, id_, uid)
    with requests.get(url) as r:# somwhow working but we usually have nothing to see.
        mdata = r.text
        mdata = json.loads(mdata)
        if mdata["ok"] == 1: # what is this ok?
            for elem in mdata["data"]:
                elem0 = {}
                elem0["text"] = elem["text"]
                if with_user:
                    userMeta = elem["user"]
                    userMeta = {k:userMeta[k] for k in ["id","name"]}
                    elem0["user"] = userMeta
                elem0["like_counts"] = elem["like_counts"]
                elem0["comments"] = []
                for comm in elem[
                    "comments"
                ]:  # also have reply_comment, though i don't know what it really means here.
                    comm0 = {}
                    comm0["text"] = comm["text"]
                    if with_user:
                        userMeta2 = comm["user"]
                        userMeta2 = {k:userMeta2[k] for k in ["id","name"]} # we don't fancy things here
                        comm0["user"] = userMeta2
                    comm0["like_count"] = comm["like_count"]
                    elem0["comments"].append(comm0)
                feedback["comments"].append(elem0)
        else:
            print(json.dumps(mdata,indent=4))
            print("NOT OK WITH WEIBO FEEDBACK!")
        return feedback


@decorator
def weiboFeedback(content,with_user=False):
    mfeedback = {}  # ordered by the blog id.
    # it will create shit after all. debug first.
    for key in content:
        mfeedback[key] = []
        print("feedback key:",key)
        print("feedback value:",content[key])
        for blog in content[key]:
            review = blog["review"] # what is this heck?
            meta = review["meta"]
            print("feedback meta:")
            print(json.dumps(meta,indent=4))
            feedback = review["feedback"] # what is this update?
            data = weiboCheckFeedback(meta,with_user=with_user)
            feedback.update(data)
            mfeedback[key].append({"meta": meta, "feedback": feedback})
    return mfeedback
