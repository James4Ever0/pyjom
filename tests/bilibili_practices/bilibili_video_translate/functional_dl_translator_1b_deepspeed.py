# loadable or not?
# OOM ready?
# maybe you want to load this shit over kaggle.
# 3521MB on inference. does that mean you can do the big fucker now?
# 1.9G model size.
import os

# mt = dlt.TranslationModel(modelpath, model_family="m2m100",device="gpu") # OOM?


from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

# model = M2M100ForConditionalGeneration.from_pretrained(modelpath)

# model_inputs = tokenizer(text_to_translate, return_tensors="pt")

# translate to French
# gen_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("en"))
# print(tokenizer.batch_decode(gen_tokens, skip_special_tokens=True))

# either load model with trainer or just use some other stuffs.

#!/usr/bin/env python

# This script demonstrates how to use Deepspeed ZeRO in an inference mode when one can't fit a model
# into a single GPU
#
# 1. Use 1 GPU with CPU offload
# 2. Or use multiple GPUs instead
#
# First you need to install deepspeed: pip install deepspeed
#
# Here we use a 3B "bigscience/T0_3B" model which needs about 15GB GPU RAM - so 1 largish or 2
# small GPUs can handle it. or 1 small GPU and a lot of CPU memory.
#
# To use a larger model like "bigscience/T0" which needs about 50GB, unless you have an 80GB GPU -
# you will need 2-4 gpus. And then you can adapt the script to handle more gpus if you want to
# process multiple inputs at once.
#
# The provided deepspeed config also activates CPU memory offloading, so chances are that if you
# have a lot of available CPU memory and you don't mind a slowdown you should be able to load a
# model that doesn't normally fit into a single GPU. If you have enough GPU memory the program will
# run faster if you don't want offload to CPU - so disable that section then.
#
# To deploy on 1 gpu:
#
# deepspeed --num_gpus 1 t0.py
# or:
# python -m torch.distributed.run --nproc_per_node=1 t0.py
#
# To deploy on 2 gpus:
#
# deepspeed --num_gpus 2 t0.py
# or:
# python -m torch.distributed.run --nproc_per_node=2 t0.py


from transformers import AutoConfig
from transformers.deepspeed import HfDeepSpeedConfig
import deepspeed
import os
import torch

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # To avoid warnings about parallelism in tokenizers

# distributed setup
local_rank = int(os.getenv("LOCAL_RANK", "0"))
world_size = int(os.getenv("WORLD_SIZE", "1"))
torch.cuda.set_device(local_rank)
deepspeed.init_distributed()

# model_name = "bigscience/T0_3B"
modelpath = "/media/root/Jumpcut/person_segmentation/paraphraser/m2m100_1.2B"

config = AutoConfig.from_pretrained(modelpath)
model_hidden_size = config.d_model

# batch size has to be divisible by world_size, but can be bigger than world_size
train_batch_size = 1 * world_size

# ds_config notes
#
# - enable bf16 if you use Ampere or higher GPU - this will run in mixed precision and will be
# faster.
#
# - for older GPUs you can enable fp16, but it'll only work for non-bf16 pretrained models - e.g.
# all official t5 models are bf16-pretrained
#
# - set offload_param.device to "none" or completely remove the `offload_param` section if you don't
# - want CPU offload
#
# - if using `offload_param` you can manually finetune stage3_param_persistence_threshold to control
# - which params should remain on gpus - the larger the value the smaller the offload size
#
# For indepth info on Deepspeed config see
# https://huggingface.co/docs/transformers/main/main_classes/deepspeed

# keeping the same format as json for consistency, except it uses lower case for true/false
# fmt: off
ds_config = {
    "fp16": {
        "enabled": True # to half the model precision.
    },
    "zero_optimization": {
        "stage": 3,
        "offload_param": {
            "device": "cpu",
            "pin_memory": True
        },
        "overlap_comm": True,
        "contiguous_gradients": True,
        "reduce_bucket_size": model_hidden_size * model_hidden_size,
        "stage3_prefetch_bucket_size": 0.9 * model_hidden_size * model_hidden_size,
        "stage3_param_persistence_threshold": 10 * model_hidden_size
    },
    "steps_per_print": 2000,
    "train_batch_size": train_batch_size,
    "train_micro_batch_size_per_gpu": 1,
    "wall_clock_breakdown": False
}
# fmt: on

# next line instructs transformers to partition the model directly over multiple gpus using
# deepspeed.zero.Init when model's `from_pretrained` method is called.
#
# **it has to be run before loading the model AutoModelForSeq2SeqLM.from_pretrained(model_name)**
#
# otherwise the model will first be loaded normally and only partitioned at forward time which is
# less efficient and when there is little CPU RAM may fail
dschf = HfDeepSpeedConfig(ds_config)  # keep this object alive

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
# now a model can be loaded.
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

model = M2M100ForConditionalGeneration.from_pretrained(modelpath)
# this will not fuck shit up.

# initialise Deepspeed ZeRO and store only the engine object
ds_engine = deepspeed.initialize(model=model, config_params=ds_config)[0]
ds_engine.module.eval()  # inference

# Deepspeed ZeRO can process unrelated inputs on each GPU. So for 2 gpus you process 2 inputs at once.
# If you use more GPUs adjust for more.
# And of course if you have just one input to process you then need to pass the same string to both gpus
# # If you use only one GPU, then you will have only rank 0.
# rank = torch.distributed.get_rank()
# if rank == 0:
#     text_in = "Is this review positive or negative? Review: this is the best cast iron skillet you will ever buy"
# elif rank == 1:
#     text_in = "Is this review positive or negative? Review: this is the worst restaurant ever"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# sentence = "你吃饭了没有" # You have eaten. from m2m100 418M

tokenizer = M2M100Tokenizer.from_pretrained(modelpath,src_lang="en",tgt_lang="zh")

# source = tokenizer.get_lang_id("zh")
# tokenizer.src_lang = source
mdevice = torch.device("cuda")
# tokenizer.to(mdevice)


# inputs = tokenizer.encode(text_in, return_tensors="pt").to(device=local_rank)

def get_response(sentence):
    text_to_translate =sentence

    model_inputs = tokenizer(text_to_translate, return_tensors="pt")

    # inputs = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("en"))

    model_inputs = {k:model_inputs[k].to(mdevice) for k in model_inputs.keys()}

    with torch.no_grad():
        # outputs = ds_engine.module.generate(inputs, synced_gpus=True)
        while True:
            try:
                gen_tokens = ds_engine.module.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("zh"),synced_gpus=True,do_sample=True).cpu() # whatever. no too heavy lifting.
                # gen_tokens = ds_engine.module.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("zh"),synced_gpus=True,do_sample=True,top_k=0,num_beams=8,num_return_sequences=1,no_repeat_ngram_size=2,temperature=1.4).cpu() # whatever.
                # gen_tokens = ds_engine.module.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("zh"),synced_gpus=True,do_sample=True,top_k=0,top_p=0.92,num_beams=5,num_return_sequences=5,no_repeat_ngram_size=2,temperature=0.7).cpu() # whatever.
                break
            except:
                import traceback
                traceback.print_exc()
                breakpoint() # translate speed is slow as hell. must do some summarization. or you cover them all.
                # you may do this for pictures.
    # text_out = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("TRANSLATED:")
    return tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)


# print(get_response("你吃饭了没有"))
# print("PROMPT READY.")
# print("type exit to exit.")
# while True:
#     targetSentence = input("\nprompt>")
#     if "exit" not in targetSentence:
#         result = get_response(targetSentence)
#         print(result) # this is goddamly working. fuck!
#     else:
#         break

# import time
# values = []
# for _ in range(3):
#     a = time.time()
#     translate_once()
#     b = time.time()
#     value = b-a
#     # value = timeit.timeit(stmt="translate_once()")
#     print("TIME COST: {}".format(value))
#     values.append(value)
# print("TOTAL COST:",values)
# print("AVERAGE COST:",sum(values)/len(values))
# stuck at the end.
# TOTAL COST: [6.2853310108184814, 4.705244541168213, 4.688654661178589]
# AVERAGE COST: 5.226410071055095
# better not to use swap.