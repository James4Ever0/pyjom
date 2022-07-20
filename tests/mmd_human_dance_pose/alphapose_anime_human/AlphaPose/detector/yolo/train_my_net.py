from darknet import Darknet
from torch.optim import AdamW
from torch.nn import CrossEntropyLoss
import argparse

def arg_parse():
    """
    Parse arguements to the detect module
    
    """
    
    
    parser = argparse.ArgumentParser(description='YOLO v3 Video Detection Module')
   
    parser.add_argument("--video", dest = 'video', help = 
                        "Video to run detection upon",
                        default = "video.avi", type = str)
    parser.add_argument("--dataset", dest = "dataset", help = "Dataset on which the network has been trained", default = "pascal")
    parser.add_argument("--confidence", dest = "confidence", help = "Object Confidence to filter predictions", default = 0.5) # lower the freaking confidence.
    # we need to retrain this fuck.
    # how to? use my bounding box generator. no manual labeling. but we first need to understand the training process.
    parser.add_argument("--nms_thresh", dest = "nms_thresh", help = "NMS Threshhold", default = 0.4)
    parser.add_argument("--cfg", dest = 'cfgfile', help = 
                        "Config file",
                        default = "cfg/yolov3-spp.cfg", type = str)
    parser.add_argument("--weights", dest = 'weightsfile', help = 
                        "weightsfile",
                        default = "data/yolov3-spp.weights", type = str)
    parser.add_argument("--reso", dest = 'reso', help = 
                        "Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
                        default = "416", type = str)
    parser.add_argument("--device", dest = 'device', help = 
                        "compute device",
                        default = "cuda", type = str)
    return parser.parse_args()

cfgfile = "cfg/yolov3-spp.cfg"
weightsfile = "data/yolov3-spp.weights"

picture = "/media/root/help/pyjom/samples/image/miku_on_green.png"

reso = 416
model = Darknet(cfgfile)
model.load_weights(weightsfile)
print("Network successfully loaded")

model.net_info["height"] = reso
import numpy as np
import torch
args = arg_parse()
# swear that is not good.
from torch.autograd import Variable
import cv2
img = cv2.imread(picture)
input_dim = reso
from video_demo import prep_image
# img = cv2.resize(img, (input_dim, input_dim)) 
img_ = prep_image(img,input_dim)
# img_ =  img[:,:,::-1].transpose((2,0,1))
# img_ = img_[np.newaxis,:,:,:]/255.0
# img_ = torch.from_numpy(img_).float()
# output = model(Variable(img_),args)
print(output)
print(output.shape)
# torch.Size([1, 10647, 85])
# what is this shit for? why the hell you have other shits?