# 加载模型
from transformers import T5Tokenizer, T5ForConditionalGeneration

modelID = "ClueAI/PromptCLUE-base-v1-5"
# https://github.com/James4Ever0/transformers/blob/main/src/transformers/models/auto/configuration_auto.py
# https://github.com/James4Ever0/transformers/blob/main/src/transformers/modeling_utils.py (need change)


tokenizer = T5Tokenizer.from_pretrained(modelID, local_files_first=True)
model = T5ForConditionalGeneration.from_pretrained(
    modelID, local_files_first=True
)  # oh shit! 1G model
# print("TOKENIZER?", tokenizer) # always cpu. no "device" attribute.
# print("_"*20)
# print("MODEL?", model.device)
# breakpoint()
# what are these devices? all default CPU?


def preprocess(text):
    return text.replace("\n", "_")


def postprocess(text):
    return text.replace("_", "\n")


def answer(text, sample=True, top_p=0.8, device="cpu"):
    """sample：是否抽样。生成任务，可以设置为True;
    top_p：0-1之间，生成的内容越多样"""
    text = preprocess(text)
    encoding = tokenizer(
        text=[text], truncation=True, padding=True, max_length=768, return_tensors="pt"
    ).to(device)
    if not sample:
        out = model.generate(
            **encoding,
            return_dict_in_generate=True,
            output_scores=False,
            max_length=128,
            num_beams=4,
            length_penalty=1
        )
    else:
        out = model.generate(  # check "generate_config" in test.py?
            **encoding,
            return_dict_in_generate=True,
            output_scores=False,
            max_length=128,
            min_length=5,
            do_sample=True,
            length_penalty=1,
            num_beams=4,
            top_p=top_p
        )
    out_text = tokenizer.batch_decode(out["sequences"], skip_special_tokens=True)
    return postprocess(out_text[0])


def my_function():
    # Function code goes here
    q = """重写句子：
支持几十个不同类型的任务，具有较好的零样本学习能力和少样本学习能力。
答案：
"""  # i think this model just doesn't get it.
    output = answer(q)
    print("Output:", output)


import timeit

# Time the function
elapsed_time = timeit.timeit(my_function, number=1)

print("Elapsed time:", elapsed_time)
# Elapsed time: 10.513529631891288
# not too bad?
