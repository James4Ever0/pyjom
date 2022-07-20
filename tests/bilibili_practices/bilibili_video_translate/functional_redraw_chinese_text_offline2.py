use_cuda_cv2 = True # after we compile shit

if use_cuda_cv2: # the freaking speed is awful.
    import pathlib
    import site
    import sys

    # this is root. this is not site-packages.

    # site_path = pathlib.Path([x for x in site.getsitepackages() if "site-packages" in x][0])
    site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages") # maybe it is done after you make install the whole cv2 shit.
    cv2_libs_dir = site_path / 'cv2' / f'python-{sys.version_info.major}.{sys.version_info.minor}'
    print(cv2_libs_dir)
    cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
    if len(cv2_libs) == 1:
        print("INSERTING:",cv2_libs[0].parent)
        sys.path.insert(1, str(cv2_libs[0].parent))


import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw  
import Levenshtein
import math
# from m2m100_1b_translator import zh_to_en_translator as translator
# i just want to do the freaking inpainting.
# import statistics

def redraw_english_to_chinese2(image,resultChineseInternal): 
    a,b,c = image.shape

    total_area = a*b
    total_center = (a/2,b/2)
    total_corners = [(a,0),(0,0),(0,b),(a,b)]
    total_strings = ["scorpa"]
    area_threshold = 1/15 # don't know.
    area_threshold = total_area*area_threshold

    mask3_threshold = area_threshold*0.6

    blank_image = np.zeros(shape=[a,b], dtype=np.uint8) # the exact order
    blank_image2 = np.zeros(shape=[a,b], dtype=np.uint8) # the exact order
    blank_image3 = np.zeros(shape=[a,b], dtype=np.uint8) # the exact order
    def compareStringSimilarity(text,targetCompareString="scorpa"):
        # what is this?
        comparedWaterMarkString = targetCompareString.lower() # the freaking name 
        comparedWaterMarkStringLength = len(comparedWaterMarkString)
            # remove watermarks? how to filter?
            # no fucking translation at all.
        editDistanceThreshold = 4
        textCompareCandidate = text.replace(" ","").lower() # original text, no translation.
        distance = Levenshtein.distance(textCompareCandidate,comparedWaterMarkString)
        string_length = len(text)
        string_length_difference = abs(string_length-comparedWaterMarkStringLength)
        length_difference_threshold = 3
        if (distance < editDistanceThreshold and string_length_difference < length_difference_threshold):
            return True
        return False
    def get_center(rectangle_coords):
        x0,y0 = rectangle_coords[0]
        x1,y1 = rectangle_coords[2]
        return ((x0+x1)/2,(y0+y1)/2)
    def get_distance(a,b): x = a[0]-b[0]; x2 = x**2; y = a[1]-b[1];y2 = y**2; return(math.sqrt(x2+y2))
    resultChineseInternal2 = list(sorted(resultChineseInternal,key=lambda x:min([get_distance(corner,get_center(x[0])) for corner in total_corners]))) # sort by centrality. but not by corner. use corner instead.
    resultChineseInternal2 = sorted(resultChineseInternal2,key=lambda x:1-max([int(compareStringSimilarity(x[1][0],tstring)) for tstring in total_strings])) # sort by centrality. but not by corner. use corner instead.
    for coords, (text,prob) in resultChineseInternal2: # get boundary coords first.
        polyArray = np.array(coords).astype(np.int64) # fuck.
        # print(polyArray)
        # print(polyArray.shape)
        # breakpoint()
        # points = np.array([[160, 130], [350, 130], [250, 300]])
        # print(points.dtype)
        # points = np.array([[454.0, 22.0], [464.0, 26.0], [464.0, 85.0]]).astype(np.int64)
        # this is rectangular. simple shit. not simple for other shits.
        color= 255
        coord0, coord1, coord2 = coords[0],coords[1],coords[2]
        sid1, sid2 = get_distance(coord0,coord1), get_distance(coord1,coord2)
        polyArea = sid1*sid2
        mask3_area = np.sum(blank_image3)
        if polyArea >= area_threshold or mask3_area >= mask3_threshold:
            cv2.fillPoly(blank_image,[polyArray],color)
            isClosed = True
            thickness = 20 # oh shit.
            thickness2 = 40 # oh shit.
            cv2.polylines(blank_image, [polyArray], isClosed, color, thickness) # much better.
            cv2.polylines(blank_image2, [polyArray], isClosed, color, thickness2) # much better.
        else:
            cv2.fillPoly(blank_image3,[polyArray],color)
            isClosed = True
            thickness = 30 # oh shit.
            thickness2 = 50 # oh shit.
            # cv2.polylines(blank_image, [polyArray], isClosed, color, thickness) # much better.
            cv2.polylines(blank_image3, [polyArray], isClosed, color, thickness) # much better.
            cv2.polylines(blank_image2, [polyArray], isClosed, color, thickness2) # much better.
    #     # cv2.fillPoly(blank_image,pts=[points],color=(255, 255,255))
    # cv2.imshow("mask",blank_image)
    # cv2.waitKey(0)
    # use wordninja.
    # before translation we need to lowercase these shits.
    # inpaint_alternative = cv2.INPAINT_NS
    # dst = cv2.inpaint(image,blank_image,3,inpaint_alternative)
    def partial_blur(image0,mask,kernel=(200,200)):
        # need improvement. malnly the boundary.
        mask_total = mask
        inv_mask_total = 255-mask_total
        # mask0 = mask
        # mask0 = mask/255
        # inv_mask0 = inv_mask/255
        non_blur_image = cv2.bitwise_and(image0, image0, mask=inv_mask_total)
        blur_image0 = cv2.blur(image0,kernel) # half quicklier.
        blur_image0 = cv2.bitwise_and(blur_image0, blur_image0, mask=mask_total)
        dst0 = blur_image0 + non_blur_image
        return dst0
    def partial_blur_deprecated(image0,mask,mask2):
        # need improvement. malnly the boundary.
        mask_total = mask + mask2 # not good.
        dtype = mask.dtype
        mask_total = mask_total>0
        mask_total=mask_total.astype(dtype)
        mask_total = mask_total*255
        inv_mask_total = 255-mask_total
        mask0 = mask_total - mask2
        # mask0 = mask
        # mask0 = mask/255
        # inv_mask0 = inv_mask/255
        non_blur_image = cv2.bitwise_and(image0, image0, mask=inv_mask_total)
        blur_image0 = cv2.blur(image0,(50,50)) # half quicklier.
        blur_image2 = cv2.blur(image0,(30,30)) # half quicklier.
        # not enough baby
        blur_image0 = cv2.bitwise_and(blur_image0, blur_image0, mask=mask0)
        blur_image2 = cv2.bitwise_and(blur_image2, blur_image2, mask=mask2)
        dst0 = blur_image0 +blur_image2 + non_blur_image
        return dst0
    dst = partial_blur(image,blank_image)
    dst = cv2.inpaint(dst,blank_image3,3,cv2.INPAINT_TELEA) # this shit. only do for small areas
    dst = partial_blur(dst,blank_image2,kernel=(30,30))
    # to compensate all sharp boundaries.

    # from PIL import Image

    def np2pillow(opencv_image):
        color_coverted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(color_coverted)
        return pil_image
        # pil_image.show()

    def pillow2np(pil_image):
        # pil_image=Image.open("demo2.jpg") # open image using PIL
        # use numpy to convert the pil_image into a numpy array
        numpy_image=np.array(pil_image)  
        # convert to a openCV2 image, notice the COLOR_RGB2BGR which means that 
        # the color is converted from RGB to BGR format
        opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 
        return opencv_image
    # draw text now!
    mpil_image = np2pillow(dst)
    draw = ImageDraw.Draw(mpil_image)
    font_location = "/root/Desktop/works/bilibili_tarot/SimHei.ttf" # not usual english shit.
    def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255),stroke_width=1,stroke_fill=(0,0,0),align="left"):
    # Get rendered font width and height.
        draw = ImageDraw.Draw(image)
        width, height = draw.textsize(text, font=font,stroke_width=stroke_width)
        # Create a new image with transparent background to store the text.
        textimage = Image.new('RGBA', (width, height), (0,0,0,0))
        # Render the text.
        textdraw = ImageDraw.Draw(textimage)
        textdraw.text((0,0), text, font=font, fill=fill,stroke_width=stroke_width,stroke_fill=stroke_fill,align=align)
        # Rotate the text image.
        rotated = textimage.rotate(angle, expand=1) # do you rotate shit?
        # Paste the text into the image, using it as a mask for transparency.
        image.paste(rotated, position, rotated)
        return image
    def average(mlist):return sum(mlist) / len(mlist)

    def get_coord_orientation_font_size_and_center(coords):
        xlist, ylist = [x[0] for x in coords], [x[1] for x in coords]
        min_x, max_x = min(xlist), max(xlist)
        min_y, max_y = min(ylist), max(ylist)
        width,height = max_x-min_x, max_y-min_y
        position = (min_x,min_y)
        c0,c1,c2,c3 = coords
        real_width = average([get_distance(c0,c1) ,get_distance(c2,c3)])
        real_height = average([get_distance(c1,c2) ,get_distance(c3,c0)])

        # c0-------------c1
        # |              |
        # c3-------------c2

        rotate_vectors = (c1[0]-c0[0],c1[1]-c0[1]),(c2[0]-c3[0],c2[1]-c3[1])

        rotate_vector = (average([rotate_vectors[0][0],rotate_vectors[1][0]]),average([rotate_vectors[0][1],rotate_vectors[1][1]]))
        rotate_angle = math.atan2(rotate_vector[1],rotate_vector[0]) # problem with angle.
        # print("ROTATE_VECTORS:",rotate_vectors)
        # print("ROTATE VECTOR:",rotate_vector)
        # print("ROTATE ANGLE:", rotate_angle)

        center = (int((max_x+min_x)/2),int((max_y+min_y)/2))
        # what about rotation? forget about it...
        if (width / height) < 0.8:
            orientation = "vertical"
            font_size = int(real_width) # shit.
        else:
            orientation = "horizontal"
            font_size = int(real_height)
        return orientation, font_size, center,(real_width,real_height),rotate_angle,position 

    readjust_size=False # just center.

    for coords, (text,prob) in resultChineseInternal:
        probThreshold = 0.8
        if compareStringSimilarity(text) or prob < probThreshold: # this is somehow not right. i don't know.
            # mask all with low probabilities?
            continue # skip all shits.
        # specified font size 
        # text = translator(text) # now translate.
        # too freaking slow. i need to freaking change this shit.
        orientation, font_size, center ,(width,height) ,rotate_angle,position = get_coord_orientation_font_size_and_center(coords)
        if orientation == "horizontal":
            font = ImageFont.truetype(font_location, font_size)
            # text = original_text
            # drawing text size 
            stroke_width = max((1,int(0.1*font_size)))

            (string_width,string_height) = draw.textsize(text,font=font,stroke_width=stroke_width)
            # print(string_width)
            # breakpoint()
            if readjust_size:
                change_ratio = width/string_width
                new_fontsize = font_size*change_ratio
                font = ImageFont.truetype(font_location, new_fontsize)
                (string_width,string_height) = draw.textsize(text,font=font,stroke_width=stroke_width)
            #     start_x = int(center[0]-width2/2)
            #     start_y = int(center[1]-height2/2)
            # else:
            theta  =rotate_angle
            rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])

            v1 = np.array([string_width,string_height])
            v2 = np.array([string_width,-string_height])
            v3 = np.array([-string_width,-string_height])
            v4 = np.array([-string_width,string_height])
            # w = np.array([3, 4])
            vc1 = np.dot(rot, v1)
            vc2 = np.dot(rot, v2)
            vc3 = np.dot(rot, v3)
            vc4 = np.dot(rot, v4)
            # sw2 = abs(float(vc2[0])) # no abs.
            # sh2 = abs(float(vc2[1]))

            start_x_arr = [int(center[0]-sw/2) for sw in [(float(x[0])) for x in [vc1,vc2,vc3,vc4]]]
            start_y_arr = [int(center[1]-sh/2) for sh in [(float(x[1])) for x in [vc1,vc2,vc3,vc4]]]
            # start_y = int(center[1]-string_height2/2)
            start_x = int(min(start_x_arr))
            start_y = int(min(start_y_arr))
            # draw.text((start_x, start_y), text, font = font, fill=(255,255,255),stroke_fill=(0,0,0),stroke_width = stroke_width,align ="left") # what is the freaking align?
            position2 = (start_x, start_y)
            rotate_angle2 = -np.rad2deg(rotate_angle) # strange.
            # debug_text = "angle: {}".format(rotate_angle2)
            mpil_image = draw_rotated_text(mpil_image,text,position2,rotate_angle2,font,stroke_width=stroke_width)

    # mpil_image.show()
    # mpil_image.save("redraw_eng_to_chinese.png")
    output_final_image = pillow2np(mpil_image)
    return output_final_image