import cv2
import numpy as np
import itertools
import uuid
 
# Reading the required image in
# which operations are to be done.
# Make sure that the image is in the same
# directory in which this python program is
# video_file = "../../samples/video/LiEIfnsvn.mp4" # this one with cropped boundaries.
video_file = "/media/root/help1/pyjom/samples/video/LiGE8vLuX.mp4"

video = cv2.VideoCapture(video_file)

def rectMerge(oldRect, newRect,delta_thresh = 0.1):
    # if very much alike, we merge these rects.
    # what about those rect that overlaps? we check exactly those who overlaps.
    # 1. check all new rects against all old rects. if they overlap, highly alike (or not) then mark it as having_alike_rect (or not) and append to new old rect list. <- after those old rects have been marked with alike sign, one cannot revoke the sign. still remaining new rects will be checked against them.
    # 2. while checking, if not very alike then append newRect to new rect list.
    # 3. if one old rect has not yet been checked as having_alike_rect then cut its life. otherwise extend its life, though not extend above max_rect_life.
    (old_x1,old_y1), (old_x2, old_y2) = oldRect
    (new_x1,new_y1), (new_x2, new_y2) = newRect

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

def rectSurge(oldRectList, newRectList,delta_thresh = 0.1, min_rect_life = 0, max_rect_life = 6):
    newToOldDictList = []
    oldRectDictList = [{"rect":x["rect"], "alike":False, "life":x["life"],"uuid":x["uuid"]} for x in oldRectList] # actually they are all dict lists. you can pass an empty list as oldRectList anyway.
    # print("OLDRECTDICTLIST:",oldRectDictList)
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

def updateTotalRects(oldTotalRectDict,rectList,currentFrameIndex,diffFrame):
    for elem in rectList:
        uuid = elem["uuid"]
        rect = elem["rect"]
        if uuid not in oldTotalRectDict.keys():
            oldTotalRectDict.update({uuid:{"rect":rect,"startFrame":currentFrameIndex,"endFrame":None,"meanDifference":None}}) # finally,remove those without endFrame.
        else:
            duration = currentFrameIndex - oldTotalRectDict[uuid]["startFrame"]
            (x0,y0),(x1,y1) = rect
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
            if duration == 1:
                oldTotalRectDict[uuid]["meanDifference"] = std_total
            else:
                dur2 = duration - 1
                prev_std = oldTotalRectDict[uuid]["meanDifference"]
                new_std = (dur2*prev_std + std_total)/duration # may freaking exceed limit.
                oldTotalRectDict[uuid]["meanDifference"] = new_std
            oldTotalRectDict[uuid]["endFrame"] = currentFrameIndex
    return oldTotalRectDict

total_rect_dict ={}
rect_dict_main_list = []
min_rect_life_display_thresh = 3 # a filter.

mode = 1
line_thresh =  150
includeBoundaryLines = True # applied to those cornered crops.
# this will slow down the process. or maybe?
frameIndex = -1
prevFrame = None
if mode == 1:
    import pybgs as bgs
    algorithm = (
    bgs.FrameDifference()
)  # this

while True:
    ret, img = video.read()

    if img is None:
        if mode == 1:
            popKeys = []
            for key in total_rect_dict.keys():
                elem = total_rect_dict[key]
                if elem["endFrame"] is None:
                    popKeys.append(key)
            for key in popKeys:
                total_rect_dict.pop(key) # remove premature rectangles.
        break
    else: frameIndex+=1
    if mode == 1:
        diff_img_output = algorithm.apply(img)
    # what about the freaking still image?
    # Convert the img to grayscale
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # no need to use gray image.
    
    # Apply edge detection method on the image
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred,20,210,apertureSize = 3) # great.

    # why not applying edges directly to rectangles?
    
    # This returns an array of r and theta values

    # line_thresh =  200
    # maintain a rectangle list. merge the alikes?

    if mode == 1:
        lines = cv2.HoughLines(edges,1,np.pi/180,line_thresh)
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
        if len(mlines["horizontal"]) < 2 or len(mlines["vertical"]) < 2:
            print("unable to form rectangles.")
            continue
        else:
            rects =[] # list of rectangles
            for line_h1, line_h2 in itertools.combinations(mlines["horizontal"],2):
                ymin, ymax = list(sorted([line_h1[1],line_h2[1]]))
                for line_v1, line_v2 in itertools.combinations(mlines["vertical"], 2):
                    xmin, xmax = list(sorted([line_v1[0],line_v2[0]]))
                    rect = ((xmin,ymin),(xmax,ymax))
                    rects.append(rect)
            rect_dict_main_list = rectSurge(rect_dict_main_list,rects)
            # print("RECT DICT MAIN LIST:")
            # print(rect_dict_main_list) # maybe i want this shit?
            total_rect_dict = updateTotalRects(total_rect_dict,rect_dict_main_list,frameIndex,diff_img_output)
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
    elif mode == 2:
        lines = cv2.HoughLinesP(edges,1,np.pi/180,line_thresh,minLineLength=2,maxLineGap=100) # these are not angle filtering.
        for points in lines:
      # Extracted points nested in the list
            x1,y1,x2,y2=points[0]
            # filter out angle errors?
            # Draw the lines joing the points
            # On the original image
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            # Maintain a simples lookup list for points
            # lines_list.append([(x1,y1),(x2,y2)])
    elif mode == 3:
        # edges = cv2.GaussianBlur(edges, (5, 5), 0)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
        detect_horizontal = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)

        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
        detect_vertical = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel, iterations=3)

        cnts_horizontal = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_horizontal = cnts_horizontal[0] if len(cnts_horizontal) == 2 else cnts_horizontal[1]

        cnts_vertical = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_vertical = cnts_vertical[0] if len(cnts_vertical) == 2 else cnts_vertical[1]

        for c in cnts_horizontal:
            cv2.drawContours(img, [c], -1, (255,0,0), 3)
        
        for c in cnts_vertical:
            cv2.drawContours(img, [c], -1, (255,0,0), 3)

    # what the heck?
    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    # why you have middle lines?

            # how to get the intersections? lines?
    cv2.imshow('linesDetected.jpg', img)
    # cv2.imshow("edges.jpg",edges) # not for fun.
    if cv2.waitKey(20) == ord("q"):
        print("QUIT INTERFACE.")
        break
# All the changes made in the input image are finally
# written on a new image houghlines.jpg
if mode == 1:
    print("FINAL RESULT:")


    for key in total_rect_dict.keys():
        elem = total_rect_dict[key]
        print("RECT UUID",key)
        print("RECT CONTENT",elem)