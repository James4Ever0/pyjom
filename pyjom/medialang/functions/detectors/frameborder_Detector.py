from .mediaDetector import *
import numpy as np
import cv2
import pybgs as bgs
import talib
import uuid
import itertools
import copy

# consider merging this project with autoup, or just borrow some of its content.
# assume you not to run many instances at once?
# how to identify same video in a sequence?
# maybe you can paint translated words with paddleocr?

# framedifference can only be applied to videos, not freaking images.
def huffline_stillImage_Identifier(mediapath,**config): # wtf?
    img = cv2.imread(mediapath)
    line_thresh =  config["line_thresh"]
    includeBoundaryLines = config["includeBoundaryLines"] # applied to those cornered crops.\
    blurKernel = config["blurKernel"]
    blurred = cv2.GaussianBlur(img,blurKernel, 0)
    edges = cv2.Canny(blurred,20,210,apertureSize = 3) # great.

    lines = cv2.HoughLines(edges,1,np.pi/180,line_thresh)
    angle_error = config["angle_error"]   # this can only detect square things, absolute square.
    # we need to know horizontal and vertical lines, when they cross we get points.
    frameHeight, frameWidth = img.shape[:2]
    # print("height: ", frameHeight)
    # print("width: ", frameWidth)
    mlines = {"horizontal":[], "vertical":[]}
    if includeBoundaryLines:
        originPoint = (0,0)
        cornerPoint = (frameWidth,frameHeight)
        mlines["horizontal"].append(originPoint)
        mlines["horizontal"].append(cornerPoint)
        mlines["vertical"].append(originPoint)
        mlines["vertical"].append(cornerPoint)
    if lines is None: lines = []
    for line in lines:
        for r_theta in line:
            # breakpoint()
            r,theta = r_theta.tolist()
            # Stores the value of cos(theta) in a
            # filter detected lines?
            # theta filter:
            if not abs(theta % (np.pi/2) )< angle_error:
                continue # this is filtering.
            # print("line parameter:",r,theta)
            a = np.cos(theta)
        
            # Stores the value of sin(theta) in b
            b = np.sin(theta)
            
            # x0 stores the value rcos(theta)
            x0 = a*r
            
            # y0 stores the value rsin(theta)
            y0 = b*r
            
            # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
            x1 = int(x0 + 1000*(-b))
            
            # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
            y1 = int(y0 + 1000*(a))
        
            # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
            x2 = int(x0 - 1000*(-b))
            
            # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
            y2 = int(y0 - 1000*(a))
            
            # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
            # (0,0,255) denotes the colour of the line to be
            #drawn. In this case, it is red.
            df_x = abs(x1-x2)
            df_y = abs(y1-y2)

            lineType = "vertical"
            if df_x > df_y:
                lineType = "horizontal"
            # we just need one single point and lineType.
            linePoint = (x1,y1)
            mlines[lineType].append(linePoint)
            # cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)
            # would not draw lines this time. draw found rects instead.
    # get rectangle points. or just all possible rectangles?
    # enumerate all possible lines.
    rects =[] # list of rectangles
    if len(mlines["horizontal"]) < 2 or len(mlines["vertical"]) < 2:
        # print("unable to form rectangles.")
        # return [] # no rect.
        pass
    else:
        for line_h1, line_h2 in itertools.combinations(mlines["horizontal"],2):
            ymin, ymax = list(sorted([line_h1[1],line_h2[1]]))
            for line_v1, line_v2 in itertools.combinations(mlines["vertical"], 2):
                xmin, xmax = list(sorted([line_v1[0],line_v2[0]]))
                rect = ((xmin,ymin),(xmax,ymax))
                rects.append(rect)
        # print("RECT DICT MAIN LIST:")
        # print(rect_dict_main_list) # maybe i want this shit?
    return rects

def huffline_horizontal_vertical_FrameIterator(mediapath,**config):
    video_file = mediapath # this one with cropped boundaries.

    video = cv2.VideoCapture(video_file)

    def rectMerge(oldRect, newRect,delta_thresh = config["delta_thresh"]):
        # if very much alike, we merge these rects.
        # what about those rect that overlaps? we check exactly those who overlaps.
        # 1. check all new rects against all old rects. if they overlap, highly alike (or not) then mark it as having_alike_rect (or not) and append to new old rect list. <- after those old rects have been marked with alike sign, one cannot revoke the sign. still remaining new rects will be checked against them.
        # 2. while checking, if not very alike then append newRect to new rect list.
        # 3. if one old rect has not yet been checked as having_alike_rect then cut its life. otherwise extend its life, though not extend above max_rect_life.
        (old_x1,old_y1), (old_x2, old_y2) = oldRect
        (new_x1,new_y1), (new_x2, new_y2) = newRect

        # too many rects?
        old_w = old_x2-old_x1
        old_h = old_y2-old_y1

        det_x1 = abs(new_x1 - old_x1)/ old_w
        det_x2 = abs(new_x2 - old_x2)/ old_w
        det_y1 = abs(new_y1 - old_y1)/ old_h
        det_y2 = abs(new_y2 - old_y2)/ old_h
        # print("deltas:",det_x1, det_x2, det_y1, det_y2)

        having_alike_rect =  (det_x1 < delta_thresh) and (det_y1 < delta_thresh) and (det_x2 < delta_thresh ) and (det_y2 < delta_thresh)

        myRect = newRect
        if having_alike_rect:
            myRect = oldRect
        
        return myRect, having_alike_rect

    def rectSurge(oldRectList, newRectList,diff_img_output,delta_thresh = config["delta_thresh"], min_rect_life = config["min_rect_life"], max_rect_life = config["max_rect_life"],max_rect_list_length = 30, rect_area_threshold = 0.05):
        yd,xd = diff_img_output.shape
        aread = yd*xd
        min_area_thresh = rect_area_threshold * aread
        def getRectArea(rect):
            (x0,y0),(x1,y1) = rect
            return (x1-x0)*(y1-y0)
        
        def getDiff(rect,diff_img_output):
            (x0,y0),(x1,y1) = rect
            diff_area = diff_img_output[y0:y1,x0:x1]
            return np.sum(diff_area)
        
        def getScore(rect,totalArea,r0=2,r1=5,key="rect"):
            # if key:
            #     rect = x["rect"]
            # else: rect = x
            area = getRectArea(rect)
            diff = getDiff(rect,diff_img_output)
            val1 = diff/area
            val2 = diff/totalArea
            return r0*val1+r1*val2

        newToOldDictList = []
        oldRectDictList = [{"rect":x["rect"], "alike":False, "life":x["life"],"uuid":x["uuid"]} for x in oldRectList if getRectArea(x["rect"]) > min_area_thresh] # actually they are all dict lists. you can pass an empty list as oldRectList anyway.
        newRectList = [x for x in newRectList if getRectArea(x) > min_area_thresh] # get something else.
        oldRectDictList = list(reversed(sorted(oldRectDictList,key=lambda x: getScore(x["rect"],aread))))[:max_rect_list_length]
        newRectList = list(reversed(sorted(newRectList,key=lambda x: getScore(x,aread))))[:max_rect_list_length]
        # oldRectDictList = sorted(oldRectDictList,key=lambda x:getRectArea(x["rect"]), reverse=True) # not good since we got other freaking shits.

        # print("OLDRECTDICTLIST:",oldRectDictList)
        # print("NEW RECT LENGTH:",len(newRectList))
        for newRect in newRectList:
            needAppend = True
            for index, oldRectDict in enumerate(oldRectDictList):
                # print("ENUMERATING OLD INDEX:",index)
                oldRect = oldRectDict["rect"]
                _, having_alike_rect = rectMerge(oldRect,newRect,delta_thresh=delta_thresh)
                if having_alike_rect:
                    needAppend = False
                    if not oldRectDict["alike"]:
                        # print("SET ALIKE:",index,oldRect)
                        oldRectDictList[index]["alike"] = True
                    # ignore myRect.
            if needAppend:
                newToOldDictList.append({"rect":newRect,"life":1,"uuid":str(uuid.uuid4())}) # make sure it is not duplicated?
                # if appended we shall break this loop. but when shall we append?
        oldToOldDictList = []
        # print("OLD RECT LENGTH:",len(oldRectDictList))

        for oldRectDict in oldRectDictList:
            alike = oldRectDict["alike"]
            life = oldRectDict["life"]
            oldRect = oldRectDict["rect"]
            myUUID = oldRectDict["uuid"]
            if not alike:
                life -=1
            else:
                life +=1
                life = min(max_rect_life, life)
            if life <= min_rect_life:
                continue
            oldToOldDictList.append({"rect":oldRect,"life":life,"uuid":myUUID})
        return oldToOldDictList + newToOldDictList # a combination.

    def updateTotalRects(oldTotalRectDict,rectList,currentFrameIndex,diffFrame,minRectArea = 1):
        for elem in rectList:
            uuid = elem["uuid"]
            rect = elem["rect"]
            (x0,y0),(x1,y1) = rect
            rectArea = (x1-x0)*(y1-y0)
            if rectArea <minRectArea:
                continue
            if uuid not in oldTotalRectDict.keys():
                oldTotalRectDict.update({uuid:{"rect":rect,"startFrame":currentFrameIndex,"endFrame":None,"meanDifference":None}}) # finally,remove those without endFrame.
            else:
                duration = currentFrameIndex - oldTotalRectDict[uuid]["startFrame"]
                # filter rect areas.
                diff = diffFrame[y0:y1,x0:x1] # this is shit. we need to crop this shit.
                # grayscale.
                # std = np.abs(std)
                # get the total delta over time?
                # std = np.mean(std,axis=2)
                diff_x = np.mean(diff.flatten())
                # std_x = np.std(std,axis=2)
                # std_x = np.std(std_x,axis=1)
                # std_x = np.std(std_x,axis=0)
                std_total = diff_x # later we need to convert this float64.
                # breakpoint()
                if std_total is None:
                    print("RECT:",rect)
                    breakpoint()
                prev_std = oldTotalRectDict[uuid]["meanDifference"]
                if duration == 1:
                    oldTotalRectDict[uuid]["meanDifference"] = std_total
                elif prev_std is None:
                    oldTotalRectDict[uuid]["meanDifference"] = std_total
                else:
                    dur2 = duration - 1
                    try:
                        new_std = (dur2*prev_std + std_total)/duration # may freaking exceed limit.
                    except:
                        print("dur2",dur2)
                        print("prev_std",prev_std)
                        print("std_total",std_total)
                        print("duration",duration)
                        breakpoint()
                    oldTotalRectDict[uuid]["meanDifference"] = new_std
                oldTotalRectDict[uuid]["endFrame"] = currentFrameIndex
        return oldTotalRectDict

    total_rect_dict ={}
    rect_dict_main_list = []
    min_rect_life_display_thresh = config["min_rect_life_display_thresh"] # a filter.

    # mode = 1
    line_thresh = config["line_thresh"]
    includeBoundaryLines = config["includeBoundaryLines"] # applied to those cornered crops.
    # this will slow down the process. or maybe?
    frameIndex = -1
    prevFrame = None
    # if mode == 1:
    # import pybgs as bgs
    algorithm = (
    bgs.FrameDifference()
    )  # this
    framePeriod = config["framePeriod"]
    config_minRectArea = config["minRectArea"]
    frame_total_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # print("FRAME_TOTAL_COUNT:",frame_total_count)
    # breakpoint()
    ocr_period = 10
    ocr_result = []
    # from .subtitleDetector import getPaddleOCR
    from shapely.geometry import Point, Polygon
    def checkPointInOcrRect(ocr_result,point,span=0):
        xp,yp = point
        p = Point(xp,yp)
        for ocr_rect in ocr_result:
            # print("OCR_RECT", ocr_rect)
            # breakpoint()
            # if certainty < certainty_thresh: continue
            p0,p1,p2,p3 = ocr_rect
            p0 = (p0[0]-span,p0[1]-span)
            p1 = (p1[0]+span,p1[1]-span)
            p2 = (p2[0]+span,p2[1]+span)
            p3 = (p3[0]-span,p3[1]+span) # it is float.
            plist = [(x[0],x[1]) for x in [p0,p1,p2,p3]]
            poly = Polygon(plist)
            if poly.contains(p):
                return True
        return False
    
    def checkLineIntersectOcrRect(ocr_result,linepoint,linetype,span=0):
        xp,yp = linepoint
        # p = Point(xp,yp)
        for ocr_rect in ocr_result:
            # print("OCR_RECT", ocr_rect)
            # breakpoint()
            # if certainty < certainty_thresh: continue
            p0,p1,p2,p3 = ocr_rect
            p0 = (p0[0]-span,p0[1]-span)
            p1 = (p1[0]+span,p1[1]-span)
            p2 = (p2[0]+span,p2[1]+span)
            p3 = (p3[0]-span,p3[1]+span) # it is float.
            plist = [(x[0],x[1]) for x in [p0,p1,p2,p3]]
            if linetype == "vertical":
                xlist = [x[0] for x in plist]
                xmin,xmax = min(xlist),max(xlist)
                if xp >=xmin and xp <= xmax:
                    return True
            else:
                ylist = [x[1] for x in plist]
                ymin,ymax = min(ylist),max(ylist)
                if yp >= ymin and yp <= ymax:
                    return True
            # poly = Polygon(plist)
            # if poly.contains(p):
            #     return True
        return False

    for _ in progressbar.progressbar(range(frame_total_count)):
        ret, img = video.read()
        # if frameIndex% ocr_period == 0:
        #     ocr_result = getPaddleOCR(img,cls=True,rec=False)
        if img is None:
            # if mode == 1:
            popKeys = []
            for key in total_rect_dict.keys():
                elem = total_rect_dict[key]
                if elem["endFrame"] is None:
                    popKeys.append(key)
            for key in popKeys:
                total_rect_dict.pop(key) # remove premature rectangles.
            break
        else: frameIndex+=1
        if not frameIndex % framePeriod == 0:
            continue# do shit.
        # if mode == 1:
        diff_img_output = algorithm.apply(img)
        # what about the freaking still image?
        # Convert the img to grayscale
        # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # no need to use gray image.
        
        # Apply edge detection method on the image
        blurred = cv2.GaussianBlur(img, config["blurKernel"], 0)
        edges = cv2.Canny(blurred,20,210,apertureSize = 3) # great.

        # why not applying edges directly to rectangles?
        
        # This returns an array of r and theta values

        # line_thresh =  200
        # maintain a rectangle list. merge the alikes?

        # if mode == 1:
        lines = cv2.HoughLines(edges,1,np.pi/180,line_thresh)
        if lines is None:
            lines = []
        angle_error = 0.00003   # this can only detect square things, absolute square.
        # we need to know horizontal and vertical lines, when they cross we get points.
        frameHeight, frameWidth = img.shape[:2]
        # print("height: ", frameHeight)
        # print("width: ", frameWidth)
        mlines = {"horizontal":[], "vertical":[]}
        if includeBoundaryLines:
            originPoint = (0,0)
            cornerPoint = (frameWidth,frameHeight)
            mlines["horizontal"].append(originPoint)
            mlines["horizontal"].append(cornerPoint)
            mlines["vertical"].append(originPoint)
            mlines["vertical"].append(cornerPoint)
        # lineTrans = {}
        for line in lines:
            for r_theta in line:
                # breakpoint()
                r,theta = r_theta.tolist()
                # Stores the value of cos(theta) in a
                # filter detected lines?
                # theta filter:
                if not abs(theta % (np.pi/2) )< angle_error:
                    continue # this is filtering.
                # print("line parameter:",r,theta)
                a = np.cos(theta)
            
                # Stores the value of sin(theta) in b
                b = np.sin(theta)
                
                # x0 stores the value rcos(theta)
                x0 = a*r
                
                # y0 stores the value rsin(theta)
                y0 = b*r
                
                # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
                x1 = int(x0 + 1000*(-b))
                
                # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
                y1 = int(y0 + 1000*(a))
            
                # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
                x2 = int(x0 - 1000*(-b))
                
                # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
                y2 = int(y0 - 1000*(a))
                
                # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
                # (0,0,255) denotes the colour of the line to be
                #drawn. In this case, it is red.
                df_x = abs(x1-x2)
                df_y = abs(y1-y2)

                lineType = "vertical"
                if df_x > df_y:
                    lineType = "horizontal"
                # we just need one single point and lineType.
                linePoint = (x1,y1)
                # for p_rect in rect:
                
                mlines[lineType].append(linePoint)
                # mlines2[lineType].append([(x1,y1), (x2,y2)])
                # lineTrans.update({str((x1,y1)+lineType):(x2,y2)})
                # cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)
                # would not draw lines this time. draw found rects instead.
        # get rectangle points. or just all possible rectangles?
        yd,xd = diff_img_output.shape
        # print("IMAGE SHAPE",xd,yd)
        rangeLimitRatio = 0.1
        # rangeLimit = 
        visual=False
        for lineType in mlines.keys():
            dropIndexs = []
            data0 =mlines[lineType]
            if lineType == "vertical":
                selectedPoints = [x[0] for x in data0]
                rangeLimit = xd*rangeLimitRatio
                selectedRanges = list_to_range(selectedPoints,rangeLimit)
                # print(selectedRanges)
                selectedRangesFlattened = [x for y in selectedRanges for x in y]
                # print(selectedRangesFlattened)
                data0 = [x for x in data0 if x[0] in selectedRangesFlattened]
            else:
                selectedPoints = [x[1] for x in data0]
                rangeLimit = yd*rangeLimitRatio
                selectedRanges = list_to_range(selectedPoints,rangeLimit)
                selectedRangesFlattened = [x for y in selectedRanges for x in y]
                data0 = [x for x in data0 if x[1] in selectedRangesFlattened]
            # for index, linePoint in enumerate(data0):
            #     # linePoint = mlines[lineType]
            #     if checkLineIntersectOcrRect(ocr_result,linePoint,lineType): dropIndexs.append(index)
            # newdata0 = [data0[i] for i in range(len(data0)) if i not in dropIndexs]
            newdata0 = data0
            mlines[lineType] = newdata0
            if visual:
                for linePoint in newdata0:
                    (x1,y1) = linePoint
                    # (x2,y2) = lineTrans[str((x1,y1))+lineType]
                    if lineType == "vertical":
                        x2 = x1
                        y2 = yd
                    else:
                        x2 = xd
                        y2 = y1
                    cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)
        # enumerate all possible lines.

        if len(mlines["horizontal"]) < 2 or len(mlines["vertical"]) < 2:
            # print("unable to form rectangles.")
            continue
        else:
            rects =[] # list of rectangles
            eliminateRatio = 0.3
            for line_h1, line_h2 in itertools.combinations(mlines["horizontal"],2): # this is a problem.
                ymin, ymax = list(sorted([line_h1[1],line_h2[1]]))
                yspan = ymax-ymin
                if yspan < yd*eliminateRatio:
                    continue
                for line_v1, line_v2 in itertools.combinations(mlines["vertical"], 2): # this is a problem.
                    xmin, xmax = list(sorted([line_v1[0],line_v2[0]]))
                    rect = ((xmin,ymin),(xmax,ymax))
                    # pr1,pr2 = rect
                    # for p_rect in rect:
                    #     if checkPointInOcrRect(ocr_result,p_rect): continue # skip those traitors.
                    xspan = xmax-xmin
                    if xspan < xd*eliminateRatio:
                        continue
                    rects.append(rect)
            # for index,elem in enumerate(rect_dict_main_list):

            rect_dict_main_list = rectSurge(rect_dict_main_list,rects,diff_img_output)
            # print("RECT DICT MAIN LIST:")
            # print(rect_dict_main_list) # maybe i want this shit?
            total_rect_dict = updateTotalRects(total_rect_dict,rect_dict_main_list,frameIndex,diff_img_output,minRectArea=config_minRectArea)
            mdisplayed_rect_count = 0
            for rect_dict in rect_dict_main_list:
                life = rect_dict["life"]
                if life < min_rect_life_display_thresh:
                    continue # this is needed.
                # draw shit now.
                mdisplayed_rect_count +=1
                (xmin,ymin),(xmax,ymax) = rect_dict["rect"]
                cv2.rectangle(img,(xmin,ymin),(xmax,ymax) , (255,0,0), 2)
            #     (xmin,ymin),(xmax,ymax) = rect
            #     rect_area = (xmax-xmin) * (ymax-ymin)
            #     print("rect found:",rect,rect_area)
            prevFrame = img.copy()
            # print("total rects:",mdisplayed_rect_count)
        if visual:
            cv2.imshow('linesDetected.jpg', img)
            # cv2.imshow("edges.jpg",edges) # not for fun.
            if cv2.waitKey(20) == ord("q"):
                print("QUIT INTERFACE.")
                break
    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    # if mode == 1:
    print("FINAL RESULT:")
    for key in total_rect_dict.keys():
        elem = total_rect_dict[key]
        print("RECT UUID",key)
        print("RECT CONTENT",elem)
    popKeys = []
    for key in total_rect_dict.keys():
        elem = total_rect_dict[key]
        if elem["endFrame"] is None:
            popKeys.append(key)
    for key in popKeys:
        total_rect_dict.pop(key) # remove premature rectangles.
    # break
    return total_rect_dict

def framedifference_talib_FrameIterator(mediapath,**config):
    algorithm = (
        bgs.FrameDifference()
    )  # this is not stable since we have more boundaries. shall we group things?
    video_file = (
        mediapath  # this is doggy video without borders.
    )
    # video_file = "../../samples/video/LiEIfnsvn.mp4" # this one with cropped boundaries.

    capture = cv2.VideoCapture(video_file)
    while not capture.isOpened():
        capture = cv2.VideoCapture(video_file)
        # cv2.waitKey(1000)
        # print("Wait for the header")

    pos_frame = capture.get(1)
    past_frames = config["past_frames"]


    def getAppendArray(mx1, min_x, past_frames=past_frames):
        return np.append(mx1[-past_frames:], min_x)


    def getFrameAppend(frameArray, pointArray, past_frames=past_frames):
        mx1, mx2, my1, my2 = [
            getAppendArray(a, b, past_frames=past_frames)
            for a, b in zip(frameArray, pointArray)
        ]
        return mx1, mx2, my1, my2

    timeperiod = config["timeperiod"]
    def getStreamAvg(a, timeperiod=timeperiod):  # to maintain stability.
        return talib.stream.EMA(a, timeperiod=timeperiod)

    change_threshold = config["change_threshold"]
    def checkChange(frame_x1, val_x1, h, change_threshold=change_threshold):
        return (abs(frame_x1 - val_x1) / h) > change_threshold  # really changed.


    mx1, mx2, my1, my2 = [np.array([]) for _ in range(4)]
    # past_frames = 19
    #already set.
    perc = config["perc"]
    frame_num = 0 # not to change.
    # what is the time to update the frame?

    frame_x1, frame_y1, frame_x2, frame_y2 = [None for _ in range(4)]
    reputation = 0
    max_reputation = config["max_reputation"]
    minVariance =config["minVariance"]

    frameDict = {}  # include index, start, end, coords.

    frameIndex = 0
    framePeriod = config["framePeriod"]
    frame_total_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # print("FRAME_TOTAL_COUNT:",frame_total_count)
    # breakpoint()
    for _ in progressbar.progressbar(range(frame_total_count)):
        flag, frame = capture.read()
        if not frameIndex%framePeriod == 0:
            continue # skip shit.
        frameIndex += 1
        if flag:
            pos_frame = capture.get(1)  # this is getting previous frame without read again.
            img_output = algorithm.apply(frame)
            img_bgmodel = algorithm.getBackgroundModel()
            _, contours = cv2.findContours(
                img_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )
            # maybe you should merge all active areas.
            if contours is not None:
                # continue
                counted = False
                for contour in contours:
                    [x, y, w, h] = cv2.boundingRect(img_output)
                    if not counted:
                        min_x, min_y = x, y
                        max_x, max_y = x + w, y + h
                        counted = True
                    else:
                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        max_x = max(max_x, x + w)
                        max_y = max(max_y, y + h)
                        # only create one single bounding box.
                # print("points:",min_x, min_y, max_x,max_y)
                this_w = max_x - min_x
                this_h = max_y - min_y
                thresh_x = max(minVariance, int(perc * (this_w)))
                thresh_y = max(minVariance, int(perc * (this_h)))
                mx1, mx2, my1, my2 = getFrameAppend(
                    (mx1, mx2, my1, my2), (min_x, max_x, min_y, max_y)
                )
                val_x1, val_x2, val_y1, val_y2 = [
                    getStreamAvg(a) for a in (mx1, mx2, my1, my2)
                ]
                # not a number. float
                # will return False on any comparison, including equality.
                if (
                    abs(val_x1 - min_x) < thresh_x
                    and abs(val_x2 - max_x) < thresh_x
                    and abs(val_y1 - min_y) < thresh_y
                    and abs(val_y2 - max_y) < thresh_y
                ):
                    needChange = False
                    # this will create bounding rect.
                    # this cannot handle multiple active rects.
                    reputation = max_reputation
                    if frame_x1 == None:
                        needChange = True
                    elif (
                        checkChange(frame_x1, val_x1, this_w)
                        or checkChange(frame_x2, val_x2, this_w)
                        or checkChange(frame_y1, val_y1, this_h)
                        or checkChange(frame_y2, val_y2, this_h)
                    ):
                        needChange = True
                        # the #2 must be of this reason.
                    if needChange:
                        frame_x1, frame_y1, frame_x2, frame_y2 = [
                            int(a) for a in (min_x, min_y, max_x, max_y)
                        ]
                        print()
                        print("########FRAME CHANGED########")
                        frame_num += 1
                        frame_area = (frame_x2 - frame_x1) * (frame_y2 - frame_y1)
                        # update the shit.
                        coords = ((frame_x1, frame_y1), (frame_x2, frame_y2))
                        frameDict[frame_num] = {
                            "coords": coords,
                            "start": frameIndex,
                            "end": frameIndex,
                        }
                        print(
                            "FRAME INDEX: {}".format(frame_num)
                        )  # this is the indexable frame. not uuid.
                        print("FRAME AREA: {}".format(frame_area))
                        print("FRAME COORDS: {}".format(str(coords)))
                    # allow us to introduce our new frame determinism.
                else:
                    if reputation > 0:
                        reputation -= 1
                if frame_x1 is not None and reputation > 0:
                    # you may choose to keep cutting the frame? with delay though.
                    cv2.rectangle(
                        frame, (frame_x1, frame_y1), (frame_x2, frame_y2), (255, 0, 0), 2
                    )
                    frameDict[frame_num]["end"] = frameIndex
                    # we mark the first and last time to display this frame.
                # how to stablize this shit?
            cv2.imshow("video", frame)
            # just video.
            # cv2.imshow('img_output', img_output)
            # cv2.imshow('img_bgmodel', img_bgmodel)

        else:
            # cv2.waitKey(1000) # what the heck?
            break
        # if 0xFF & cv2.waitKey(10) == 27:
        #     break
    # cv2.destroyAllWindows()
    print("FINAL FRAME DETECTIONS:")
    print(frameDict)
    return frameDict
    # {1: {'coords': ((80, 199), (496, 825)), 'start': 13, 'end': 269}, 2: {'coords': ((80, 381), (483, 644)), 'start': 297, 'end': 601}}


def frameborder_default_configs(model="framedifference_talib"):
    assert model in ["framedifference_talib","huffline_horizontal_vertical"]
    if model == "framedifference_talib":
        df_config = {"past_frames":19,"timeperiod":10, "change_threshold":0.2,"perc":0.03, "max_reputation": 3,"framePeriod":1,"minVariance" :10}
    else:
        df_config = {"line_thresh":150, # original 150
        "includeBoundaryLines":True,"blurKernel":(5,5),"angle_error":0.00003,"delta_thresh":0.1,"min_rect_life":0,"max_rect_life":6,"framePeriod":1,"min_rect_life_display_thresh":3,"minRectArea":1}
    return df_config


def frameborder_Detector(mediapaths, model="framedifference_talib",config={}):
    print("MODEL:",model)
    # breakpoint()
    yconfig = copy.deepcopy(config)
    # breakpoint()
    # if config is None:
    #     breakpoint()
    #     config = {}
    # any better detectors? deeplearning?
    assert model in ["framedifference_talib","huffline_horizontal_vertical"]
    results = []
    keyword = "{}_detector".format(model)
    data_key = keyword # different than yolo.
    for mediapath in mediapaths:
        print("mediapath:", mediapath)
        breakpoint()
        mediatype = getFileType(mediapath)
        print("subtitle of mediatype:", mediatype)
        assert mediatype in ["video", "image"]  # gif? anything like that?
        if model == "framedifference_talib":
            assert mediatype == "video"
            # advice you to check out only those areas with rectangles, not something else, if detected any rectangular area.
            # but does that happen for normal videos? you might want huffline transforms.
            # you can eliminate unwanted rectangles by time duration and huffline transforms.
        result = {"type": mediatype, data_key: {}}
        default_config = frameborder_default_configs(model)
        xconfig = default_config
        xconfig.update(yconfig) # override default configs.
        # do not freaking assign directly after update.
        config = xconfig
        # print("YCONFIG:", yconfig)
        # breakpoint()

        if mediatype == "image":
            data = cv2.imread(mediapath)
            data = keywordDecorator(huffline_stillImage_Identifier, **config)(data) # this is just oldfashioned function decorator
            result[data_key].update({keyword: data})
            result[data_key].update({"config": config})
        else:
            # you may not want videoFrameIterator.
            if model == "framedifference_talib":
                mdata= framedifference_talib_FrameIterator(
                    mediapath,**config)
            elif model == "huffline_horizontal_vertical":
                mdata = huffline_horizontal_vertical_FrameIterator(mediapath,**config)
            metadata = {"config": config}
            result[data_key][keyword] = mdata
            result[data_key].update(metadata)
            results.append(result)
    return results
