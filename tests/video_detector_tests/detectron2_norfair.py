import cv2
import numpy as np
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from cocoNames import cocoRealName

from norfair import Detection, Tracker, Video, draw_tracked_objects

def euclidean_distance(detection, tracked_object):
    return np.linalg.norm(detection.points - tracked_object.estimate)

# Set up Detectron2 object detector
cfg = get_cfg()
cfg.merge_from_file("norfair/demos/faster_rcnn_R_50_FPN_3x.yaml")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 # looks like it does not recognize dog.
# cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"
cfg.MODEL.WEIGHTS = "/root/Desktop/works/pyjom/tests/video_detector_tests/detectron2_models/model_final_f10217.pkl"
# it is stored in s3
# https://dl.fbaipublicfiles.com/detectron2/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl

# download cache: /root/.torch/iopath_cache/detectron2/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl

detector = DefaultPredictor(cfg)
# what are the classes output by the model?

# Norfair
video_path = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
# video_path = "/root/Desktop/works/pyjom/samples/video/LlfeL29BP.mp4"
video = Video(input_path=video_path)
tracker = Tracker(distance_function=euclidean_distance, distance_threshold=400,hit_inertia_min=2,hit_inertia_max=20,initialization_delay=1) # what the heck?


tracked_objects = None
display=True
for index, frame in enumerate(video): # we need to speed up.
    if index%10 == 0:
        detections = detector(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        print("original detections:",detections)
        instances = detections["instances"]
        print("instances:",instances)
        # breakpoint()
        pred_classes = instances.pred_classes
        if len(pred_classes) == 0:
            continue
        detections2=[]
        for index,class_ in enumerate(pred_classes):
            print("index:",index)
            class_ = int(class_.cpu().numpy().tolist())
            print("class:",class_)
            box = instances.pred_boxes.tensor[index].cpu().numpy().tolist()
            box = [int(x) for x in box]
            score = float(instances.scores[index].cpu().numpy().tolist())
            print('box:',box)
            print('score:',score)
            className = cocoRealName[class_]
            # we filter our targets.
            if className not in ["person","dog"]:
                continue
            mdata = {"box":box,"class":{"id":class_,"name":className}}
            det = Detection(instances.pred_boxes.get_centers()[index].cpu().numpy(),scores=np.array([score]),data=mdata)
            detections2.append(det)
            # breakpoint()
        # detections = [Detection(p) for p in instances.pred_boxes.get_centers().cpu().numpy()] # what is this instance anyway?
        # you would lost data you dick!
        print("detections2",detections2)
        tracked_objects = tracker.update(detections=detections2)
        # print(detections)
        print("tracked objects:",tracked_objects) # you don't track shit?
    if tracked_objects is not None:
        if tracked_objects!=[]:
            # there is no bounding box avaliable?
            for obj in tracked_objects:
                point = obj.estimate[0]
                position = tuple(point.astype(int))
                color = (255,0,0)
                # breakpoint()
                name = obj.last_detection.data["class"]["name"]
                cv2.circle(
                        frame,
                        position,
                        radius=100,
                        color=color,
                        thickness=2,
                    )
                cv2.putText(
                    frame,
                    "[{}][{}]".format(str(obj.id),name),
                    (position[0]-100,position[1]),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (0,255,0),
                    3,
                    cv2.LINE_AA,
                )
            # breakpoint()
        # i want to draw you in a different way.
        # draw_tracked_objects(frame, tracked_objects,color=(255,0,0))
    if display:
        cv2.imshow("window",frame)
        key  =  cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
        # maybe we shall print this shit somehow.
    # video.write(frame) # you write what?
if display:
    cv2.destroyAllWindows()
