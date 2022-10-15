# duplicate -> remove, do not insert
# not duplicate -> get the data, insert

# you want to clear the collection after this run?

from pymilvus import connections
from functools import lru_cache

@lru_cache(maxsize=1)
def connectMilvusDatabase(alias="default", host="localhost", port="19530"):
	connection = connections.connect(alias=alias, host=host, port=port)# can we reconnect?
	print('milvus connected')

# connectMilvusDatabase()
# connectMilvusDatabase() # will not connect again.
from pymilvus import Collection
from pymilvus import utility
from pymilvus import CollectionSchema, FieldSchema, DataType

import traceback

def getMilvusVideoDeduplicationCollection(get_existing:bool=True): # most of the time we just use the same 
    collection_name = "video_deduplication"
    try:
        if utility.has_collection(collection_name):  # be prudent.
            if get_existing:
                return Collection(collection_name)
            utility.drop_collection(collection_name)
    except:
        traceback.print_exc()
        print("maybe the collection does not exist")
    video_semantic_id = FieldSchema(  # how to insert this shit without prior knowledge?
        name="video_semantic_id",
        dtype=DataType.INT64,
        is_primary=True,  # if is primary, will do check for 'not duplicate' or something.
        auto_id=True,  # no need for id generation.
    )
    video_length = FieldSchema(
        name="video_length",
        dtype=DataType.FLOAT,
    )
    video_phash = FieldSchema(
        name="video_phash", dtype=DataType.BINARY_VECTOR, dim=64
    )  # 64
    # single dimension? no multi dimension support?
    schema = CollectionSchema(
        fields=[video_semantic_id, video_length, video_phash],
        description="Test video deduplication",
    )

    collection = Collection(
        name=collection_name,
        schema=schema,
        using="default",
        shards_num=2,
    )
    # is this demo collection?
    return collection

# seems hard to setup.
# not started!
# https://milvus.io/docs/v2.0.0/metric.md#binary
# the metric is important to us.
import numpy as np
import bitarray


def transformVideoPhash(videoPhash):
    # we need the raw phash.
    queryData = np.array(
        videoPhashTruthTable8x8
    )
    queryData = queryData.reshape(-1).tolist()
    queryData = ["1" if x else "0" for x in queryData]

    queryData = bitarray.bitarray("".join(queryData), endian="little")
    queryData = queryData.tobytes()
    return queryData
# dimension: 8*8=64

def indexVideoWithVideoDurationAndPhash(collection, videoDuration, videoPhash):
    queryData = transformVideoPhash(videoPhash)
    collection.insert([[np.float32(videoDuration)], [queryData]])
# can release even if not loaded.

def indexVideoWithVideoDurationAndPhashFromFile(collection, videoFilePath):
    videoDuration = 
    videoPhash = 
    indexVideoWithVideoDurationAndPhash(collection, videoDuration, videoPhash)
    return videoDuration, videoPhash


def reloadMilvusCollection(collection):
    collection.release() # unload.
    collection.load()
# make it into some library!

# insert after load?

# # 1,64
# what is wrong? wtf?
# queryData = queryData.tolist()
def searchDuplicatedVideoInMilvusByFile(collection,videoFilePath,search_params = {"metric_type": "Jaccard", "params": {"nprobe": 10}}, autoreload:bool=True):
    if autoreload:
        reloadMilvusCollection(collection)
    minVideoLength = max(0, videoDuration - span)
    maxVideoLength = videoDuration +span
    results = collection.search(
        data=[queryData],  # this is the float dimension.
        anns_field="video_phash",
        param=search_params,
        output_fields=["video_length"],
        limit=10,
        expr="video_length > {minVideoLength} and video_length < {maxVideoLength}".format(minVideoLength=minVideoLength, maxVideoLength=maxVideoLength),
        # expr='video_length < 1.2',
    )
    theHit = results[0]
# print(theHit)
# so we can perform search without filtering afterwards.
# results[0][0].entity.get('video_length')
# print(results[0].ids)
# now, we want to have the 'distance' parameter.
# print(results[0])
# print(theHit)
# distances = theHit.distances
# results = [x for x in theHit]
# hits = len(theHit)
# breakpoint()
# how to get document by id? wtf
