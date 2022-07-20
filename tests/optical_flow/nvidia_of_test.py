from nvidia_common import *
import numpy as np 
import cv2
import flow_vis

video_file = "/media/root/help/pyjom/samples/video/dog_with_text.mp4"
# this is the fastest.

video = cv2.VideoCapture(video_file)

ret, img = video.read()
prevImg = img.copy()

while True:
    ret, img = video.read()
    if img is None: break
    else:
        frame1 = prevImg
        frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        frame2 = img # why freaking grayscale?
        frame2 =  cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        prevImg = img.copy()

        perfPreset = 5
        gpuId=0
        # nvof = cv2.cuda_NvidiaOpticalFlow_2_0.create((frame1.shape[1], frame1.shape[0]),5, False, False, False, 0)
        gpu_flow =cv2.cuda_FarnebackOpticalFlow.create(5, 0.5, False,
                                                        15, 3, 5, 1.2, 0)

        gpu_frame_a = cv2.cuda_GpuMat()
        gpu_frame_b = cv2.cuda_GpuMat()
        gpu_frame_a.upload(frame1)
        gpu_frame_b.upload(frame2)

        # -- exec flow --
        gpu_flow = cv2.cuda_FarnebackOpticalFlow.calc(gpu_flow, gpu_frame_a,
                                                      gpu_frame_b, None)

        gpu_flow = gpu_flow.download()
        # gpu_flow = gpu_flow.transpose(2,0,1)
        # print(gpu_flow.shape())
        # breakpoint()
        # gpu_flow = th.from_numpy(gpu_flow).half()
    

        # cv2.writeOpticalFlow('OpticalFlow.flo', flowUpSampled)

        visualize = flow_vis.flow_to_color(gpu_flow, convert_to_bgr=False)
        cv2.imshow("OPTFLOW",visualize)
        if cv2.waitKey(20) == chr("q"):
            print("QUIT THIS SHIT")
            break
        # nvof.collectGarbage()