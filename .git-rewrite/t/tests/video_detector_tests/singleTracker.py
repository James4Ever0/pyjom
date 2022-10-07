import cv2
# import imutils #another dependency?
# tracker = cv2.TrackerCSRT_create() # outdated tracker.
# i really don't know what is a dog.
import torch

# don't really know how paddleocr recognize chars.
localModelDir = '/root/Desktop/works/pyjom/pyjom/models/yolov5/ultralytics_yolov5_master/'
import os
os.environ["YOLOV5_MODEL_DIR"] = '/root/Desktop/works/pyjom/pyjom/models/yolov5/'
model = torch.hub.load(localModelDir, 'yolov5s',source="local")

def getDogBB(frame,thresh=0.7):
    img = frame[:,:,::-1].transpose((2,0,1))
    # Inference
    # reshape this shit.
    # img = np.reshape()
    results = model(img) # pass the image through our model

    df = results.pandas().xyxy[0]
    print(df)

    data = []
    for index,line in df.iterrows():
        # print(line)
        left = (line["xmin"],line["ymin"])
        right = (line["xmax"],line["ymax"])
        confidence = line["confidence"]
        class_ = line["class"]
        name = line["name"]
        if name == "dog" and confidence >= thresh: # better figure out all output names.
            data.append({"location":[left,right],"confidence":confidence,"identity":{"class":class_,"name":name}})
    print(data)
    data = list(sorted(data,key=lambda x: -x["confidence"]))
    if len(data)>0:
        target= data[0]
        xmin,ymin = target["location"][0]
        xmax,ymax = target["location"][1]
        return int(xmin),int(ymin),int(xmax-xmin),int(ymax-ymin)

def checkDog(frame,thresh=0.5):
    return getDogBB(frame,thresh=thresh) == None # dog missing.
# better use something else?

# tracker = cv2.TrackerMIL_create()
tracker_types = ['MIL', 'GOTURN', 'DaSiamRPN']
tracker_type = tracker_types[2]
basepath = "./OpenCV-Object-Tracker-Python-Sample"

if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL_create()
elif tracker_type == 'DaSiamRPN': # deeplearning.
    # this tracker is slow as hell. really.
    params = cv2.TrackerDaSiamRPN_Params()
    params.model = os.path.join(basepath,"model/DaSiamRPN/dasiamrpn_model.onnx")
    params.kernel_r1 = os.path.join(basepath,"model/DaSiamRPN/dasiamrpn_kernel_r1.onnx")
    params.kernel_cls1 = os.path.join(basepath,"model/DaSiamRPN/dasiamrpn_kernel_cls1.onnx")
    tracker = cv2.TrackerDaSiamRPN_create(params)
    # tracker = cv2.TrackerDaSiamRPN_create()
elif tracker_type == 'GOTURN': #also need config file.
    # this is bad though.
    params = cv2.TrackerGOTURN_Params()
    params.modelTxt = os.path.join(basepath,"model/GOTURN/goturn.prototxt") # save this shit without BOM.
    params.modelBin = os.path.join(basepath,"model/GOTURN/goturn.caffemodel")
    tracker = cv2.TrackerGOTURN_create(params)
    # tracker = cv2.TrackerGOTURN_create()
# we have to feed dog coordinates into the shit.

video = cv2.VideoCapture("../../samples/video/dog_with_text.mp4")

_,frame = video.read()
# frame = imutils.resize(frame,width=720) #why?
index = 0
yoloRate = 10
track_success = False
update_track = 3
BB = None
init=False
while frame is not None:
    index +=1
    _, frame = video.read()
    if frame is None:
        print("VIDEO END.")
        break
    if index%yoloRate == 0:
        if BB is None:
            BB = getDogBB(frame)
        else:
            x, y, w, h = BB
            if len(frame.shape) == 3:
                dogFrame = frame[y:y+h,x:x+w,:]
            else:
                dogFrame = frame[y:y+h,x:x+w]
            result = checkDog(dogFrame)
            if result: # dog gone missing.
                BB = getDogBB(frame)
                init=False
    if BB is not None:
        if not init:
            tracker.init(frame, BB) # how to init this shit?
            init=True
    # when lost, we know there is no dog inside the bounding box.
    # frame = imutils.resize(frame,width=720)
        if index % update_track == 0:
            track_success,BB = tracker.update(frame)
        if track_success and BB:
            top_left = (int(BB[0]),int(BB[1]))
            bottom_right = (int(BB[0]+BB[2]), int(BB[1]+BB[3]))
            cv2.rectangle(frame,top_left,bottom_right,(0,255,0),5)
    cv2.imshow('Output',frame)
    key  =  cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()