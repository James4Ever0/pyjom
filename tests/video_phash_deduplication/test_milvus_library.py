# # duplicate -> remove, do not insert
# # not duplicate -> get the data, insert

# # you want to clear the collection after this run?

# from functools import lru_cache

# from pymilvus import connections

# @lru_cache(maxsize=1)
# def connectMilvusDatabase(alias="default", host="localhost", port="19530"):
#     connection = connections.connect(
#         alias=alias, host=host, port=port
#     )  # can we reconnect?
#     print("milvus connected")


# # connectMilvusDatabase()
# # connectMilvusDatabase() # will not connect again.
# from pymilvus import Collection
# from pymilvus import utility
# from pymilvus import CollectionSchema, FieldSchema, DataType

# import traceback


# def getMilvusVideoDeduplicationCollection(
#     get_existing: bool = False,
# ):  # most of the time we just use the same
#     collection_name = "video_deduplication"
#     try:
#         if utility.has_collection(collection_name):  # be prudent.
#             if get_existing:
#                 return Collection(collection_name)
#             utility.drop_collection(collection_name)
#     except:
#         traceback.print_exc()
#         print("maybe the collection does not exist")
#     video_semantic_id = FieldSchema(  # how to insert this shit without prior knowledge?
#         name="video_semantic_id",
#         dtype=DataType.INT64,
#         is_primary=True,  # if is primary, will do check for 'not duplicate' or something.
#         auto_id=True,  # no need for id generation.
#     )
#     video_length = FieldSchema(
#         name="video_length",
#         dtype=DataType.FLOAT,
#     )
#     video_phash = FieldSchema(
#         name="video_phash", dtype=DataType.BINARY_VECTOR, dim=64
#     )  # 64
#     # single dimension? no multi dimension support?
#     schema = CollectionSchema(
#         fields=[video_semantic_id, video_length, video_phash],
#         description="Test video deduplication",
#     )

#     collection = Collection(
#         name=collection_name,
#         schema=schema,
#         using="default",
#         shards_num=2,
#     )
#     # is this demo collection?
#     return collection


# # seems hard to setup.
# # not started!
# # https://milvus.io/docs/v2.0.0/metric.md#binary
# # the metric is important to us.
# import numpy as np
# import bitarray


# @lru_cache(maxsize=1)
# def transformVideoPhash(videoPhash):
#     # we need the raw phash.
#     queryData = videoPhash.hash  # videoPhashTruthTable8x8 or something
#     queryData = queryData.reshape(-1).tolist()
#     queryData = ["1" if x else "0" for x in queryData]
#     queryData = bitarray.bitarray("".join(queryData), endian="little")
#     queryData = queryData.tobytes()
#     return queryData


# # dimension: 8*8=64


# def indexVideoWithVideoDurationAndPhash(collection, videoDuration, videoPhash):
#     queryData = transformVideoPhash(videoPhash)
#     collection.insert([[np.float32(videoDuration)], [queryData]])


# # can release even if not loaded.

# from test_video_hash import getVideoPHash
# import caer


# @lru_cache(maxsize=1)
# def getVideoDurationAndPhashFromFile(videoFilePath):
#     videoDuration = caer.video.frames_and_fps.get_duration(videoFilePath)
#     videoPhash = getVideoPHash(videoFilePath)
#     return videoDuration, videoPhash


# def indexVideoWithVideoDurationAndPhashFromFile(collection, videoFilePath):
#     videoDuration, videoPhash = getVideoDurationAndPhashFromFile(videoFilePath)
#     indexVideoWithVideoDurationAndPhash(collection, videoDuration, videoPhash)


# def reloadMilvusCollection(collection):
#     collection.release()  # unload.
#     collection.load()


# # make it into some library!
# # insert after load?

# # # 1,64
# # what is wrong? wtf?
# # queryData = queryData.tolist()
# def getDistancesBySearchingDuplicatedVideoInMilvusByFile(
#     collection,
#     videoFilePath,
#     search_params={"metric_type": "Jaccard", "params": {"nprobe": 10}},
#     autoreload: bool = True,
#     span: float = 2,
#     debug: bool = False,
#     limit: int = 10,
# ):
#     if autoreload:
#         reloadMilvusCollection(collection)
#     videoDuration, videoPhash = getVideoDurationAndPhashFromFile(videoFilePath)
#     queryData = transformVideoPhash(videoPhash)
#     minVideoLength = max(0, videoDuration - span)
#     maxVideoLength = videoDuration + span
#     results = collection.search(
#         data=[queryData],  # this is the float dimension.
#         anns_field="video_phash",
#         param=search_params,
#         output_fields=["video_length"],
#         limit=limit,
#         expr="video_length > {minVideoLength} and video_length < {maxVideoLength}".format(
#             minVideoLength=minVideoLength, maxVideoLength=maxVideoLength
#         ),
#     )
#     theHit = results[0]
#     # print(theHit)
#     # so we can perform search without filtering afterwards.
#     # results[0][0].entity.get('video_length')
#     # print(results[0].ids)
#     # now, we want to have the 'distance' parameter.
#     # print(results[0])
#     # print(theHit)
#     distances = list(theHit.distances)
#     if debug:
#         print("distances: %s" % distances)

#     return distances
#     # what is the distance? we need to try.
#     # returh the closest distance?
#     # results = [x for x in theHit]
#     # hits = len(theHit)
#     # breakpoint()
#     # how to get document by id? wtf


# def checkDuplicatedVideoAndInsertVector(
#     collection,
#     videoPath,
#     threshold: float = 0.15,  # are you sure?
#     insertDuplicatedVector: bool = True,
#     debug: bool = True,
# ):
#     reloadMilvusCollection(collection)
#     distances = getDistancesBySearchingDuplicatedVideoInMilvusByFile(
#         collection, videoPath, debug=debug
#     )

#     minDistance = min(distances + [1])  # empty!
#     duplicated = minDistance < threshold
#     if insertDuplicatedVector or (not duplicated):
#         indexVideoWithVideoDurationAndPhashFromFile(
#             collection, videoPath
#         )  # anyway let's do this.
#     return duplicated


# shall we insert that vector or not, even if we have detected the duplicated media?
# you choose.
import sys
import os

# os.chdir("../../")
sys.path.append("../../")
# ignore the global proxy now, we are not going to use that.
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
from pyjom.videotoolbox import getMilvusVideoDeduplicationCollection,checkDuplicatedVideoAndInsertVector
if __name__ == "__main__":
    # connectMilvusDatabase()
    collection = (
        getMilvusVideoDeduplicationCollection()
    )  # will not get existing collections
    videoPaths = [
        "cute_cat_gif.mp4",
        "cute_cat_gif.gif",
        "cat_delogo.gif",
        "/root/Desktop/works/pyjom/samples/video/dog_with_large_text.gif",
    ]
    # for videoPath in videoPaths:
    from lazero.utils.logger import sprint

    for videoPath in videoPaths:
        print("filepath: %s" % videoPath)
        duplicated = checkDuplicatedVideoAndInsertVector(collection, videoPath)
        sprint("duplicated?", duplicated)

"""
filepath: cute_cat_gif.mp4
distances: [0.0, 0.11764705926179886, 0.11764705926179886, 0.7200000286102295, 0.7200000286102295, 0.7346938848495483, 0.7659574747085571, 0.7924528121948242]
______________________________
filepath: cute_cat_gif.gif
distances: [0.0, 0.11764705926179886, 0.11764705926179886, 0.7200000286102295, 0.7200000286102295, 0.7346938848495483, 0.7659574747085571, 0.7692307829856873]
______________________________
filepath: cat_delogo.gif
distances: [0.0, 0.11764705926179886, 0.11764705926179886, 0.7200000286102295, 0.7200000286102295, 0.7346938848495483, 0.7659574747085571, 0.7924528121948242]
______________________________
filepath: /root/Desktop/works/pyjom/samples/video/dog_with_large_text.gif
distances: [0.0, 0.6808510422706604, 0.6938775777816772, 0.6938775777816772, 0.739130437374115, 0.7692307829856873, 0.7924528121948242, 0.7924528121948242]
______________________________
"""
