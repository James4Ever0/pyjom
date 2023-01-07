title="世上所有小猫都是天使变的！"

# use our free api first. yes?
import yaml
with open("clueai_api.yaml",'r') as f:
    apiKey=yaml.load(f,Loader=yaml.FullLoader)['api_key']
    print("Key?",apiKey)

import clueai

# initialize the Clueai Client with an API Key
# 微调用户finetune_user=True
# cl = clueai.Client(apiKey)
print(cl.check_usage(finetune_user=False)) 
# shit. we are on trial.
# {'使用量': 0, '剩余量': 5000, '用户类型': '免费用户'}