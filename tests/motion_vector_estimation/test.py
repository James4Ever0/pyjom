# it contains subpixel motion vectors. fucking hell

source = "/root/Desktop/works/pyjom/samples/video/dog_with_text.mp4"
from lazero.utils.importers import cv2_custom_build_init
from sniffio import current_async_library

cv2_custom_build_init()
from mvextractor.videocap import VideoCap
from caer.video.frames_and_fps import count_frames, get_res
import cv2

framesCount = count_frames(source)
res = get_res(source)  # (width, height)
print("RES: %s" % str(res))
res_x, res_y = res

frame_common_divisor = min(res_x, res_y)
import math
def cartesianDistance(d2vector):
    x,y = d2vector
    return math.sqrt(x**2 + y**2)

def XYWHToDiagonal(x,y,w,h):
    return (x,y), (x+w,y+h)
# 如果整除16那么就在这个范围里面 如果不整除范围就要扩大 扩大到相应的16的倍数
def get16Value(res_x):
    rem_x = res_x % 16
    val = res_x // 16
    if rem_x != 0:
        val += 1
    return val

x_16val = get16Value(res_x)
y_16val = get16Value(res_y)

motion_render_frame = (x_16val*16, y_16val*16)

total_block_weights = x_16val * y_16val * 2 * 2

cap = VideoCap()
cap.open(source)  # wtf is going on here?
# if there is nothing we will breakup

visualize, show_picture = False, False

# so there can only be one such macroblock
def checkMacroBlock(value):
    for mod in [16, 8]:
        modValue = value % mod
        if modValue == mod / 2:
            return mod
    # if not satisfied, we are shit.

from functools import lru_cache

@lru_cache(maxsize=4)
def getModXModYFromBlockCenterCoordinates(blockCenterCoordinates):
    block_x, block_y = blockCenterCoordinates
    mod_x, mod_y = checkMacroBlock(block_x), checkMacroBlock(block_y)
    if mod_x is not None and mod_y is not None:
        return mod_x, mod_y
    else:
        print("block center coordinates", blockCenterCoordinates)
        print("WTF IS GOING ON WITH THE BLOCK CENTER")
        breakpoint()
        return 0,0

def getRectangleXYWHFromBlockCenterCoordinates(blockCenterCoordinates):
    block_x, block_y = blockCenterCoordinates
    mod_x, mod_y = getModXModYFromBlockCenterCoordinates(blockCenterCoordinates)
    mod_x_half, mod_y_half = mod_x/2, mod_y/2
    x,y,w,h = block_x-mod_x_half, block_y-mod_y_half, mod_x, mod_y
    return tuple([int(elem) for elem in [x,y,w,h]])

def getBlockWeightFromBlockCenterCoordinates(blockCenterCoordinates):
    mod_x, mod_y = getModXModYFromBlockCenterCoordinates(blockCenterCoordinates)
    weights = mod_x * mod_y / 8 / 8
    return weights

import progressbar
import numpy as np

# max_dst_x, max_dst_y = 0,0


def averageMotionVectors(motion_vector_list):
    if len(motion_vector_list) == 0:
        average_tuple = (0, 0)
    if len(motion_vector_list) > 1:
        marray = np.array(motion_vector_list)
        # print("MAKING AVERAGE:")
        # print(marray)
        average = np.average(marray, axis=0)
        # breakpoint()
        average_tuple = tuple(average)
    else:
        average_tuple = tuple(motion_vector_list[0])
    return average_tuple


for _ in progressbar.progressbar(range(framesCount)):
    success, frame, motion_vectors, frame_type, timestamp = cap.read()
    height, width, channels = frame.shape
    # breakpoint()
    if success:
        # what is the content of this motion vector?
        # print(motion_vectors)
        # import pandas as pd
        # df = pd.DataFrame(motion_vectors)
        # df = pd.DataFrame(motion_vectors,index=['source_index','unk0','unk1','src_x','src_y','dst_x','dst_y','motion_x','motion_y','motion_scale'])
        # breakpoint()
        # print()
        # print("_____________________________")
        condition = motion_vectors[:, 0] < 0
        # print(condition)
        # print(condition.shape)
        # breakpoint()
        motion_vectors_simplified = motion_vectors[condition, :][:, [0, 5, 6, 7, 8, 9]]
        motion_vectors_scale = motion_vectors_simplified[:, [5]]
        motion_vectors_scale_inversed = 1 / motion_vectors_scale
        motion_vectors_with_scale = motion_vectors_simplified[:, [3, 4]]
        motion_vectors_scale_inversed_stacked = np.hstack(
            [motion_vectors_scale_inversed] * 2
        )
        motion_vectors_restored = (
            motion_vectors_scale_inversed_stacked * motion_vectors_with_scale
        )  # just element wise?
        # print('STACKED:', motion_vectors_scale_inversed_stacked.shape)
        # print("WITH SCALE:", motion_vectors_with_scale.shape)
        # print("RESTORED:",motion_vectors_restored.shape)
        # print(motion_vectors_simplified.shape)
        # print(motion_vectors_scale.shape)
        # breakpoint()
        motion_vectors_dest_coords_restored = np.hstack(
            [motion_vectors_simplified[:, [1, 2]], motion_vectors_restored]
        )
        # motion_vectors_simplified = motion_vectors[:,[0,5,6,7,8]]
        # motion_vectors_simplified_unique = np.unique(motion_vectors_simplified, axis=0)
        # print(motion_vectors_simplified_unique.shape, motion_vectors.shape)
        # breakpoint()
        motion_vectors_dict = {}
        for mv in motion_vectors_dest_coords_restored:
            # drop duplicates first!
            (
                dst_x,  # corresponding macro block.
                dst_y,  # for destination only
                motion_x,
                motion_y,
                # motion_scale,  # don't know what the fuck is wrong with the motion scale
            ) = mv.tolist()
            # say we just want source_index <0, aka mv compared to previous frame
            # try:
            #     assert motion_x / motion_scale == src_x - dst_x
            #     assert motion_y / motion_scale == src_y - dst_y
            # except:
            #     print(src_x, dst_x, motion_x, motion_scale)
            #     print(src_y, dst_y, motion_y, motion_scale)
            #     print("*" * 20)
            # it will be inaccurate if we abandon this subpixel precision.
            # if source_index >= 0:
            #     continue
            # if dst_x>max_dst_x:
            #     max_dst_x = dst_x
            # if dst_y>max_dst_y:
            #     max_dst_y = dst_y
            destCoord = (dst_x, dst_y)
            motion_vector = (motion_x, motion_y)
            # print(destCoord)
            # breakpoint()
            if motion_vector == (0, 0):
                # print("zero motion vector detected. skipping")
                # breakpoint()
                continue
            # print('destination coords:',destCoord)
            # print('motion vector:',motion_vector)
            motion_vectors_dict.update(
                {destCoord: motion_vectors_dict.get(destCoord, []) + [motion_vector]}
            )
            # you know, different frame sources may lead to different results.
            # these vectors could overlap. which one you want to keep? the smaller ones or the bigger ones?

            # if destCoord in destCoords:
            #     print("SKIPPING DUPLICATE DESTCOORD:", destCoord)
            #     print("PREVIOUS MV",prevMV)
            #     print("CURRENT MV", mv)
            #     continue
            # else:
            #     destCoords.add(destCoord)
            # prevMV = mv
            # try:
            #     # src_x, src_y may not apply the same rule.
            #     # assert src_x % 16 == 8
            #     # assert src_y % 16 == 8
            #     assert checkMacroBlock(dst_x) is not None
            #     assert checkMacroBlock(dst_y) is not None
            #     # assert dst_x<=res_x # dst_x can go beyond the res_x
            #     # assert dst_y<=res_y
            #     # so all rules applied.
            # except:
            #     # print('source',src_x, src_y)
            #     print("res", res_x, res_y)
            #     print('destionation',dst_x, dst_y)
            #     print('motion',motion_x, motion_y)
            #     print("scale",motion_scale)
        motion_vectors_dict_averaged = {
            key: averageMotionVectors(motion_vectors_dict[key])
            for key in motion_vectors_dict.keys()
        }
        # assuming no duplicates?
        weighted_motion_vectors = []
        weights = []
        rectangles = []
        motion_vectors_filtered = [] # for getting data later?
        for blockCenterCoordinates, average_motion_vector in motion_vectors_dict_averaged.items():
            if average_motion_vector == (0, 0):
                continue
                # wtf is this? why fucking zero?
                # print('skipping zero average motion vector')
                # print("destination coords", key)
                # print('average motion vector', average_motion_vector)
            else:
                m_x, m_y = average_motion_vector
                motion_vectors_filtered.append(average_motion_vector)
                rectangle_XYWH = getRectangleXYWHFromBlockCenterCoordinates(blockCenterCoordinates)
                rectangles.append(rectangle_XYWH)
                blockWeight = getBlockWeightFromBlockCenterCoordinates(blockCenterCoordinates)
                weights.append(blockWeight)
                weighted_motion_vectors.append((m_x*blockWeight/frame_common_divisor, m_y*blockWeight/frame_common_divisor))
        weighted_motion_vectors = np.array(weighted_motion_vectors)
        sum_weighted_motion_vector=np.sum(weighted_motion_vectors, axis=0)
        average_global_weighted_motion_vector = sum_weighted_motion_vector/ total_block_weights
        sum_weights = sum(weights)
        average_weighted_motion_vector = sum_weighted_motion_vector / sum_weights
        motion_area_ratio = sum_weights/total_block_weights
        # print(motion_vectors.shape)
        motion_vectors_filtered_cartesian_distance = [cartesianDistance(vector) for vector in motion_vectors_filtered]+[0] # to avoid errors.

        min_cartesian = min(motion_vectors_filtered_cartesian_distance)
        max_cartesian = max(motion_vectors_filtered_cartesian_distance)

        if motion_vectors_dict_averaged != {}:
            # breakpoint()
            if visualize:
            print("motion area ratio",motion_area_ratio)
            print('average_weighted_motion_vector', average_weighted_motion_vector)
            print('average_global_weighted_motion_vector', average_global_weighted_motion_vector)
            motion_mask = np.zeros((motion_render_frame[1],motion_render_frame[0],1))
            for index, (x,y,w,h) in enumerate(rectangles):
                pt1, pt2 = XYWHToDiagonal(x,y,w,h)
                # print(pt1, pt2)
                current_cartesian = motion_vectors_filtered_cartesian_distance[index]
                # print(type(pt1), type(pt1[0]))
                relative_motion_cartesian = (current_cartesian-min_cartesian)/(max_cartesian-min_cartesian) # must from 0 to 1 so we can plot this,
                # relative_motion_cartesian = 255*((current_cartesian-min_cartesian)/(max_cartesian-min_cartesian))
                # relative_motion_cartesian = int(relative_motion_cartesian)
                # relative_motion_cartesian = min(255,max(0, relative_motion_cartesian))
                # breakpoint()
                cv2.rectangle(motion_mask, pt1, pt2, color=(relative_motion_cartesian,), thickness=-1)
            # should we gaussian blur, threshold this, do convolution and then apply bounding box on it?
            # # visualize this.
            cv2.imshow('motion_mask',motion_mask)
            cv2.waitKey(100)
            # may you create bounding box for this? for tracking motion? or not?
        # breakpoint()
    else:
        break

# print('max_dst_x', max_dst_x)
# print('max_dst_y', max_dst_y)
