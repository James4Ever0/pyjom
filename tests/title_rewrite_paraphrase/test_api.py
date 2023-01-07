import requests

target = "http://www.wzwyc.com/api.php?key="

data ={"info":"支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。"}

r = requests.post(target, data=data)
print(r.text)