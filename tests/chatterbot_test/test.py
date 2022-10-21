#!/usr/bin/python

#手动设置一些语料
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

Chinese_bot = ChatBot("Training demo")
# already trained on these shits.
# from chatterbot.trainers import ChatterBotCorpusTrainer
# Create a new trainer for the chatbot
# trainer = ChatterBotCorpusTrainer(Chinese_bot)
# trainer.train("chatterbot.corpus.chinese")
# trainer.train("chatterbot.corpus.english")
list_trainer = ListTrainer(Chinese_bot)
list_trainer.train([
    '你好',
    '你好',
    '有什么能帮你的？',
    '想买数据科学的课程',
    '具体是数据科学哪块呢？'
    '机器学习',
])

# test if the bot will say what i have taught it before.


# 测试一下
question = '你好'
print(question)
response = Chinese_bot.get_response(question)
print(response)

print("\n")

question = '请问哪里能买数据科学的课程'
print(question)
response = Chinese_bot.get_response(question)
print(response)
while True:
    question = input("> ")
    response = Chinese_bot.get_response(question)
    print(response)
