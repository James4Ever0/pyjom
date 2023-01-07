# 加载模型
from transformers import T5Tokenizer, T5ForConditionalGeneration
modelID="ClueAI/PromptCLUE-base-v1-5"

tokenizer = T5Tokenizer.from_pretrained(modelID,local_first=True)
model = T5ForConditionalGeneration.from_pretrained(modelID,local_first=True,device="cpu") # oh shit! 1G model

def preprocess(text):
  return text.replace("\n", "_")

def postprocess(text):
  return text.replace("_", "\n")

def answer(text, sample=False, top_p=0.8,device='cpu'):
  '''sample：是否抽样。生成任务，可以设置为True;
  top_p：0-1之间，生成的内容越多样'''
  text = preprocess(text)
  encoding = tokenizer(text=[text], truncation=True, padding=True, max_length=768, return_tensors="pt").to(device) 
  if not sample:
    out = model.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_length=128, num_beams=4, length_penalty=0.6)
  else:
    out = model.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_length=64, do_sample=True, top_p=top_p)
  out_text = tokenizer.batch_decode(out["sequences"], skip_special_tokens=True)
  return postprocess(out_text[0])

q = '''
生成与下列文字相同意思的句子：
支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。
答案：
'''
r = answer(q)
print(r)