import math
from torch import nn
import torch

def spatial_pyramid_pool(previous_conv, num_sample, previous_conv_size, out_pool_size):
    '''
    previous_conv: a tensor vector of previous convolution layer
    num_sample: an int number of image in the batch
    previous_conv_size: an int vector [height, width] of the matrix features size of previous convolution layer
    out_pool_size: a int vector of expected output size of max pooling layer
    
    returns: a tensor vector with shape [1 x n] is the concentration of multi-level pooling
    '''    
    # print(previous_conv.size())
    for i in range(len(out_pool_size)):
        # print(previous_conv_size)
        h_wid = int(math.ceil(previous_conv_size[0] / out_pool_size[i]))
        w_wid = int(math.ceil(previous_conv_size[1] / out_pool_size[i]))
        h_pad = (h_wid*out_pool_size[i] - previous_conv_size[0] + 1)/2 # float man.
        h_pad = math.ceil(h_pad)
        w_pad = (w_wid*out_pool_size[i] - previous_conv_size[1] + 1)/2
        w_pad = math.ceil(w_pad)
        maxpool = nn.MaxPool2d((h_wid, w_wid), stride=(h_wid, w_wid), padding=(h_pad, w_pad)) # this has no trainable parameter.
        x = maxpool(previous_conv)
        # print(x.size())
        torch.Size([20, 16, 20, 20])
        # this is it.
        if(i == 0):
            spp = x.view(num_sample,-1)
            # print("spp size:", spp.size())
        else:
            # print("size:",spp.size())
            spp = torch.cat((spp,x.view(num_sample,-1)), 1)
    return spp

if __name__ == "__main__":
    # to test the freaking video.
    for i in [200,1000]:
        w0 = h0 = i
        x = torch.rand(20,3,w0,h0) # 20 frames, 20 width, 20 height8
        # three channels? where is the optical flow layer?
        c2layer_1 = nn.Conv2d(3,4,4)
        c2_output_1 = c2layer_1(x)
        print(c2_output_1.shape)
        c2layer_2 = nn.Conv2d(4,16,20)
        c2_output_2 = c2layer_2(c2_output_1)
        print(c2_output_2.shape)
        output_num = [20]
        spp = spatial_pyramid_pool(c2_output_2,20,[int(c2_output_2.size(2)),int(c2_output_2.size(3))],output_num) # great now you have the batch size.
        print(x.shape,spp.shape) # 1,5120
        spp_lstm = spp[None,:]
        print(spp_lstm.shape) # 1,1,5120
        cnn_1 = nn.Conv1d(20,20,16,stride=2)
        cout_1 = cnn_1(spp_lstm)
        print(cout_1.shape)
        cnn_2 = nn.Conv1d(20,20,16,stride=2)
        cout_2 = cnn_2(cout_1)
        print(cout_2.shape)
        lstm_1 = nn.LSTM(1589,400)
        out_1,hid_1 = lstm_1(cout_2)
        print(out_1.shape)
        lstm_2 = nn.LSTM(400,20)
        out_2,hid_2 = lstm_2(out_1)
        print(out_2.shape)
        lstm_3 = nn.LSTM(20,2)
        out_3,hid_3 = lstm_3(out_2)
        print(out_3.shape)