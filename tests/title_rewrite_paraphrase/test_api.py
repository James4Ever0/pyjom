import requests

content:str

target_id:int =0
timeout:int=10
providers:list[str]=["http://www.wzwyc.com/api.php?key=", "http://ai.guiyigs.com/api.php?key="] # it is about to close! fuck

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
print(output)

content =  "支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。"