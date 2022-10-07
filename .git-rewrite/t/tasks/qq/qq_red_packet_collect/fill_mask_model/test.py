import os
import torch
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

from transformers import BertTokenizer, BertForMaskedLM

model_name = "hfl/chinese-macbert-base"

tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name) # where the heck is the model?

#location:
# resolved_archive_file = cached_path(...)
# already outsourced this shit.
# /root/.cache/huggingface/transformers/f350d12c99d2a8d00f4299b8e292c2248422676424702a2c45a8a3d65646f738.749c1a543002a65141e104ba5e040263fd8eabc9d2dcfb537bf681345565ef45

# first ensure there is no [MASK] or [] surrounded values. otherwise, remove these shits.
# split them using re.split and filter these shits out with re.match

inputs = tokenizer("如果今天天气[MASK][MASK]", return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits

# retrieve index of [MASK]
mask_token_indexs = (inputs.input_ids == tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0] # (tensor([5, 6]),) without [0]
# print(mask_token_indexs) #5 and 6.
for mask_token_index in mask_token_indexs:
    predicted_token_id = logits[0, mask_token_index].argmax(axis=-1)
    result = tokenizer.decode(predicted_token_id)
    print(mask_token_index,result)

# with torch.no_grad():
#     outputs = model(**inputs)
# print(dir(outputs))