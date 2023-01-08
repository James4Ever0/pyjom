import requests

def chineseParaphraserAPI(    content:str,
debug:bool=False,
    target_id:int =0,
    timeout:int=10,
    providers:list[str]=["http://www.wzwyc.com/api.php?key=", "http://ai.guiyigs.com/api.php?key="] # it is about to close! fuck. "本站于2023年2月19日关站" buy code from "1900373358"
    ):


    target = providers[
        target_id
    ]  # all the same?
    data = {"info": content}

    # target = "http://www.xiaofamaoai.com/result.php"
    # xfm_uid = "342206661e655450c1c37836d23dc3eb"
    # data = {"contents":content, "xfm_uid":xfm_uid, "agreement":"on"}
    # nothing? fuck?

    r = requests.post(target, data=data,timeout=timeout)
    output = r.text
    success = output.strip()!= content.strip()
    if debug:
        print(output)
    return output, success

content =  "支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。"
# content = "hello world"
# it is clearly translation based.
# since it did not detect source language. well that's just for fun.
output,success =chineseParaphraserAPI(content,debug=True)