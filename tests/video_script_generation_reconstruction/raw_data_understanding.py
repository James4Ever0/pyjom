# 2d understanding or 3d?
# what about the freaking audio?

import numpy as np
import torch

video_shape = (30,100,100) # thirty frames extracted.
audio_shape = (1,40000)

video2_shape = (60,200,200) # thirty frames extracted.
audio2_shape = (1,80000)

target_sentence_shape = (10,40000) # full charset. you may choose not to speak. when should you freaking speak?
target_sentence2_shape = (15,40000) # full charset. you may choose not to speak. when should you freaking speak?

# one hot encoding.
import random
target_sentence = np.array([random.randint(0,39999) for _ in range(10)])
target_sentence2 = np.array([random.randint(0,39999) for _ in range(15)])

# i really don't care how. freaking do it!

video_data = np.random.random(video_shape)
audio_data = np.random.random(audio_shape)

video2_data = np.random.random(video2_shape)
audio2_data = np.random.random(audio2_shape)
# print(data)
# I really not caring the freaking data range.
print(video_data.shape)
print(audio_data.shape)