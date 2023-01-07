import requests

content = "支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。"

target = ["http://www.wzwyc.com/api.php?key=","http://ai.guiyigs.com/api.php?key="][0] # all the same?
data ={"info":content}

# target = "http://www.xiaofamaoai.com/result.php"
# xfm_uid = "342206661e655450c1c37836d23dc3eb"
# data = {"contents":content, "xfm_uid":xfm_uid, "agreement":"on"}
# nothing? fuck?

r = requests.post(target, data=data)
print(r.text) 