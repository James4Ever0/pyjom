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
# print(cl.check_usage(finetune_user=False)) 
# shit. we are on trial.
# {'使用量': 0, '剩余量': 5000, '用户类型': '免费用户'}


# initialize the Clueai Client with an API Key
cl = clueai.Client("", check_api_key=False) # good without API key
prompt= '''
生成与下列文字相同意思的句子：
支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。
答案：
'''.format(title) #shit.
# generate a prediction for a prompt

generate_config = {
    "do_sample": True,
    "top_p": 0.8,
    "max_length": 128,
    "min_length": 5,
    "length_penalty": 1.0,
    "num_beams": 1
  }
# 如果需要自由调整参数自由采样生成，添加额外参数信息设置方式：generate_config=generate_config
prediction = cl.generate(
        model_name='clueai-base',
        prompt=prompt,generate_config=generate_config)
# 需要返回得分的话，指定return_likelihoods="GENERATION"

# print the predicted text
print('prediction: {}'.format(prediction.generations[0].text))