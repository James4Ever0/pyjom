# 2d understanding or 3d?
# what about the freaking audio?

import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn

video_shape = (20,3,100,100) # thirty frames extracted.
audio_shape = (1,40000)

video2_shape = (70,3,200,200) # thirty frames extracted. # change it!
audio2_shape = (2,120000) # no freaking padding game.

target_sentence_shape = (20,2) # full charset. you may choose not to speak. when should you freaking speak?
target_sentence2_shape = (70,2) # full charset. you may choose not to speak. when should you freaking speak?

# one hot encoding.
import random
target_sentence = np.array([random.randint(0,1) for _ in range(20)]) # do one-hot encoding please.
target_sentence2 = np.array([random.randint(0,1) for _ in range(70)])

target_sentence = np.eye(2)[target_sentence]
target_sentence2 = np.eye(2)[target_sentence2]

pad_video_shape_2 = np.zeros((20,3,200,200))
pad_sentence_2 = np.zeros((20,2))

target_sentence2 = np.concatenate([target_sentence2,pad_sentence_2])
# print(target_sentence2.shape,pad_sentence_2.shape)
# breakpoint()
# i really don't care how. freaking do it!

video_data = np.random.random(video_shape)
audio_data = np.random.random(audio_shape)

video2_data = np.random.random(video2_shape)
audio2_data = np.random.random(audio2_shape)
# print(data)

video2_data = np.concatenate([video2_data,pad_video_shape_2])
# I really not caring the freaking data range.
print(video_data.shape)
print(audio_data.shape)

from spp_module import spatial_pyramid_pool

class VideoCutNet(torch.nn.Module):
    def __init__(self,debug=True):
        super().__init__()
        self.debug = debug
        self.hidden_states=[None]
        self.audio_hidden_states = [None]
        self.va_hidden_states = [None,None]
        self.c2layer_1 = nn.Conv2d(3,4,4)
        self.c2layer_2 = nn.Conv2d(4,16,20)
        self.output_num = [20]

        # print(x.shape,spp.shape) # 1,5120

        self.cnn_1 = nn.Conv1d(2,20,16,stride=2,padding=8) # you could use this on the audio.
        self.cnn_2 = nn.Conv1d(20,16,16,stride=2,padding=8)
        self.cnn_3 = nn.Conv1d(16,30,16,stride=4,padding=8)

        self.lstm_1 = nn.LSTM(6400,1200,batch_first=True) # huge?
        # self.lstm_2 = nn.LSTM(400,20)
        # self.lstm_3 = nn.LSTM(20,2)

        self.audio_lstm_1 = nn.LSTM(2501,500,batch_first=True)
        self.video_audio_merger = nn.Linear(1700,300)
        # self.audio_lstm_2 = nn.LSTM()
        # self.audio_lstm_3 = nn.LSTM()
        self.va_lstm_2 = nn.LSTM(300,50,batch_first=True)
        self.va_lstm_3 = nn.LSTM(50,20,batch_first=True)
        self.va_linear = nn.Linear(20,2)
    
    def clear_hidden_state(self):
        self.hidden_states=[None] # no tuple.
        self.audio_hidden_states=[None] # no tuple.
        self.va_hidden_states=[None,None] # no tuple.

    def forward(self,x,audio_x):
        # with torch.autograd.set_detect_anomaly(False):
        c2_output_1 = self.c2layer_1(x)
        if self.debug:
            print(c2_output_1.shape)
        c2_output_1 = F.relu(c2_output_1)

        c2_output_2 = self.c2layer_2(c2_output_1)
        if self.debug:
            print(c2_output_2.shape)
        c2_output_2 = F.relu(c2_output_2)
        msize = int(c2_output_2.size(0))
        # print(msize)
        # breakpoint()

        spp = spatial_pyramid_pool(c2_output_2,msize,[int(c2_output_2.size(2)),int(c2_output_2.size(3))],self.output_num) # great now you have the batch size.
        spp_lstm = spp[None,:]
        spp_lstm = F.relu(spp_lstm)

        if self.debug:
            print(spp_lstm.shape) # 1,1,5120

###AUDIO
        cout_1 = self.cnn_1(audio_x)
        if self.debug:
            print("AUDIO",cout_1.shape)
        cout_1 = F.relu(cout_1)

        cout_2 = self.cnn_2(cout_1)
        if self.debug:
            print("AUDIO",cout_2.shape)
        cout_2 = F.relu(cout_2)

        cout_3 = self.cnn_3(cout_2)
        if self.debug:
            print("AUDIO",cout_3.shape)
        cout_3 = F.relu(cout_3)

        aout_1, ahid_1 = self.audio_lstm_1(cout_3,self.audio_hidden_states[0])
        self.audio_hidden_states[0] =(ahid_1[0].detach(),ahid_1[1].detach())
        if self.debug:
            print("AUDIO LSTM",aout_1.shape)
        aout_1 = F.relu(aout_1) # for audio only this time we apply this.
        

###AUDIO
        out_1, hid_1 = self.lstm_1(spp_lstm,self.hidden_states[0]) # passing no hidden state at all.
        self.hidden_states[0] =(hid_1[0].detach(),hid_1[1].detach())
        if self.debug:
            print(out_1.shape)
        out_1 = F.relu(out_1)
        # breakpoint()

##VIDEO AUDIO MERGE
        merged = torch.cat([aout_1,out_1],dim=2)
        if self.debug:
            print(merged.shape)
        mout_1 = self.video_audio_merger(merged)
        if self.debug:
            print(mout_1.shape)
        # breakpoint()

        mout_2,mhid_2 = self.va_lstm_2(mout_1,self.va_hidden_states[0])
        self.va_hidden_states[0] =(mhid_2[0].detach(),mhid_2[1].detach())
        if self.debug:
            print(mout_2.shape)

        mout_3,mhid_3 = self.va_lstm_3(mout_2,self.va_hidden_states[1])
        self.va_hidden_states[1] =(mhid_3[0].detach(),mhid_3[1].detach())
        if self.debug:
            print(mout_3.shape)
        # breakpoint()
        mout_4 = self.va_linear(mout_3)
        if self.debug:
            print(mout_4.shape)

        return mout_4

video_cut_net = VideoCutNet(debug=True).cuda()

video_data = torch.Tensor(video_data).cuda()
video_data2 = torch.Tensor(video2_data).cuda()

audio_data2 = torch.Tensor(audio2_data).cuda()
audio_data2 = audio_data2[None,:]
# must equal to 20 frames.
target_sentence = torch.Tensor(target_sentence).cuda()
target_sentence2 = torch.Tensor(target_sentence2).cuda()

criterion= nn.CrossEntropyLoss()
optim = torch.optim.Adam(video_cut_net.parameters(),lr=0.0001)
target = target_sentence
target = target_sentence[None,:]

target2 = target_sentence2
target2 = target_sentence2[None,:]
# for _ in range(240):# we pass 5 identical segments to our network, require to produce different labels.
video_cut_net.clear_hidden_state() # to make sure we can train this shit.
divisor = 30
audio_divisor = 40000
print(video_data2.shape) # ([60, 3, 100, 100])
# breakpoint()
frames2 = video_data2.shape[0]
import math
best_index = math.ceil(frames2/divisor)

for index in range(best_index):
    optim.zero_grad()
    video_data_slice = video_data2[index*divisor:(index+1)*divisor,:]
    audio_data_slice = audio_data2[:,:,index*audio_divisor:(index+1)*audio_divisor]
    print("AUDIO_DATA_SLICE",audio_data_slice.shape)
    # breakpoint()
    # use some padding for our video and label processes. make sure it is divisible by 20
    # data_input = video_data_slice

    target_slice = target2[:,index*divisor:(index+1)*divisor,:] # must be the right freaking target.
    print(video_data_slice.shape,target_slice.shape)
    # breakpoint()
    with torch.nn.utils.parametrize.cached():
        output = video_cut_net(video_data_slice,audio_data_slice)
        # print(output.shape,target_slice.shape) # 1,20,2
        # breakpoint()
        loss = criterion(output, target_slice)
        # print(loss)
        val_loss = loss.detach().cpu().numpy()
        print('CURRENT LOSS:',val_loss) # taking longer for long videos. may kill your freaking ram.
        loss.backward()
    optim.step()
    # where is the batch size? reduce it?
    # there is no batch size. this is recurrent network. must process sequentially.