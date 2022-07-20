# 2d understanding or 3d?
# what about the freaking audio?

import numpy as np
import torch

video_shape = (30,100,100) # thirty frames extracted.
audio_shape = (1,40000) # so batch size is included.

video2_shape = (60,200,200) # thirty frames extracted.
audio2_shape = (1,80000)

target_cut_shape = (30,2) # choose either beginning or to cut?
target_cut2_shape = (60,2) # choose either beginning or to cut?

import random
target_cut = np.array([random.randint(0,1) for _ in range(30)])
target_cut2 = np.array([random.randint(0,1) for _ in range(60)])

video_data = np.array(np.random.random(video_shape))
audio_data = np.array(np.random.random(audio_shape))

video2_data = np.array(np.random.random(video2_shape))
audio2_data = np.array(np.random.random(audio2_shape))
# print(data)
# I really not caring the freaking data range.
print(video_data.shape)
print(audio_data.shape)
print(target_cut2.shape)
device = torch.device("cuda")

video_data = torch.Tensor([video_data]) # to make sure the first dimension is batchsize
target_cut = torch.Tensor([target_cut])
audio_data = torch.Tensor(audio_data)

layer_1 = torch.nn.Conv2d(30,3,10) # original shape: (30,100,100)
output_1 = layer_1(video_data)
print(output_1.shape) #(1,3,91,91)

layer_2 = torch.nn.Conv2d(3,1,10)
output_2 = layer_2(output_1)
print(output_2.shape) #([1, 2, 82, 82])


layer_3 = torch.nn.MaxPool1d(4)
output_3 = layer_3(audio_data)
print(output_3.shape) # torch.Size([1, 10000]) # what is this fuck?

layer_4 = torch.nn.MaxPool2d(2)
output_4 = layer_4(output_2)
print(output_4.shape) # 1,2,41,41 freaking bad.

layer_5 = torch.nn.Sigmoid()
output_5 = layer_5(output_4)
print(output_5.shape) # 1,2,41,41

output_5 = output_5.reshape(1,41,41)

# get this reshaped.
output_5 = output_5.reshape(1,1,41*41)

rnn_layer_1 = torch.nn.RNN(41*41,41*41,3) # must have three dimensions.
rnn_output_1, rnn_hidd_1 = rnn_layer_1(output_5)
print(rnn_output_1.shape,rnn_hidd_1.shape) #tuple torch.Size([1, 41, 20]) torch.Size([3, 41, 20])

rnn_output_2, rnn_hidd_2 = rnn_layer_1(output_5,rnn_hidd_1)
print("RNN 2:",rnn_output_2.shape,rnn_hidd_2.shape)

rnn_output_3, rnn_hidd_3 = rnn_layer_1(rnn_output_1,rnn_hidd_1)
print("RNN 3:",rnn_output_3.shape,rnn_hidd_3.shape)
# final_data = 
final_layer = torch.nn.Linear(41*41,2) # the final swap.
final_data = final_layer(rnn_output_1)
print(final_data.shape)
# find the max one.
final_data = final_data.transpose(2,1)
print(final_data.shape)

# output_final_layer = torch.nn.MaxPool1d(41) 
# final_data2 = output_final_layer(final_data)
# print(final_data2.shape) # 40000,1 this is a single character. is it?