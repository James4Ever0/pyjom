#!/usr/bin/python
import os

# looks like the only option we have is to forget the dialog in the past and retrain.
# there is no native 'forget' option.

# we use md5 to represent the image.
db_path = "db.sqlite3"
if os.path.exists(db_path):
    os.remove(db_path)
# 手动设置一些语料
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

Chinese_bot = ChatBot("Training demo")
# already trained on these shits.
# these shits are not needed for our bot.
# from chatterbot.trainers import ChatterBotCorpusTrainer
# Create a new trainer for the chatbot
# trainer = ChatterBotCorpusTrainer(Chinese_bot)
# trainer.train("chatterbot.corpus.chinese")
# trainer.train("chatterbot.corpus.english")
list_trainer = ListTrainer(Chinese_bot)
trainset_0 = [
    "你好",
    "你好",
    "有什么能帮你的？",
    "想买数据科学的课程",
    "具体是数据科学哪块呢？" "机器学习",
]

import random

speakers = ["asoul", "猫猫", "小狗"]
import uuid

images = [str(uuid.uuid4()) for _ in range(4)]
embeddings = ["猫咪", "绝对领域", "涩图"]
r = lambda mlist: random.choice(mlist)
contents = ['今天倒了血霉了',"买兴业银行","和家里借钱"]
trainset_1 = [ # make sure our names/embeddings/hashes are wrapped in spaces.
    "[[speaker] {} ] [[image] {} [embedding] {} ] {}".format(
        r(speakers),r(images), r(embeddings),r(contents)
    )
    for _ in range(20)
]
list_trainer.train(trainset_0)

# test if the bot will say what i have taught it before.


# 测试一下
question = "你好"
print(question)
response = Chinese_bot.get_response(question)

print(response)

# question: will this chatbot get infinitely large so we have to train another one?

print("\n")

question = "请问哪里能买数据科学的课程"
print(question)
response = Chinese_bot.get_response(question)
print(response)
list_trainer.train(trainset_1)

while True:
    question = input("> ")
    response = Chinese_bot.get_response(question)
    print(response)
