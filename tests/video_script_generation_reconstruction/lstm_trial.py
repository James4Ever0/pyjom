from torch.nn import LSTM

import numpy as np

data = [[[1,2,3],[2,3,4],[3,5,6]]]

from torch import Tensor

data = Tensor(data)

layer_lstm = LSTM(3,1)

output_1, (hid_1_a,hid_1_b) = layer_lstm(data)
# print(len(hidden_1))
print(data.shape)
print(output_1.shape) # [1,3,10]
print(hid_1_a.shape,hid_1_b.shape)
