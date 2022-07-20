export http_proxy=""
export https_proxy=""

# this voice is great. excellent for my shit.

paddlespeech tts --input "你好，欢迎使用飞桨深度学习框架！" --output output.wav # must download models on the fly.

paddlespeech asr --lang zh --input output.wav
# 你好欢迎使用非讲深度学习框架
# how does it feel to have errors?

# left and right variables are not the same. what is that?