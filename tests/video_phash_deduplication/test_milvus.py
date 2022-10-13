# duplicate -> remove, do not insert
# not duplicate -> get the data, insert

# you want to clear the collection after this run?

# import pymilvus
from pymilvus import connections
form functools import lru_cache

@lru_cache(maxsize=1)
def connectMilvusDatabase():
	connection = connections.connect(alias="default", host="localhost", port="19530")# can we reconnect?
	print('milconnected')

connectMilvusDatabase()
connectMilvusDatabase() # will not connect again.

collection_name = "video_deduplication"


from pymilvus import Collection

# Collection(collection_name)
# remote this thing.
from pymilvus import utility

try:
    if utility.has_collection(collection_name):  # be prudent.
        utility.drop_collection(collection_name)
except:
    import traceback

    traceback.print_exc()
    print("maybe the collection does not exist")

from pymilvus import CollectionSchema, FieldSchema, DataType

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

# collection = Collection("video")      # Get an existing collection.
collection = Collection(
    name=collection_name,
    schema=schema,
    using="default",
    shards_num=2,
)
# is this demo collection?

# seems hard to setup.
# not started!
# https://milvus.io/docs/v2.0.0/metric.md#binary
# the metric is important to us.
search_params = {"metric_type": "Jaccard", "params": {"nprobe": 10}}
import numpy as np

queryData = np.array(
    [
        [True, True, True, False, False, True, False, True],
        [True, False, False, True, False, True, True, False],
        [True, False, False, True, True, False, False, True],
        [True, True, True, True, True, False, False, True],
        [True, False, False, True, False, True, True, False],
        [False, True, True, False, False, False, False, True],
        [True, True, False, False, False, True, True, False],
        [False, False, True, False, False, True, False, False],
    ]
)
queryData = queryData.reshape(-1).tolist()
queryData = ["1" if x else "0" for x in queryData]
import bitarray

queryData = bitarray.bitarray("".join(queryData), endian="little")
queryData2 = queryData.copy()
queryData2[1:4] = 0
queryData3 = queryData2.copy()
queryData2 = queryData2.tobytes()
queryData3[8:15] = 0
queryData3 = queryData3.tobytes()
queryData = queryData.tobytes()
# dimension: 8*8=64
# collection.insert([[1], [np.float32(3.5)], [queryData]])
# collection.insert([[np.float32(3.5)], [queryData]])
for _ in range(8):
    collection.insert([[np.float32(3.5)], [queryData]])
collection.insert([[np.float32(3.5)], [queryData2]])  # slight difference.
collection.insert([[np.float32(3.5)], [queryData3]])  # more difference.
# print(len(queryData), len(queryData)*8)
# # print(queryData.shape)
# breakpoint()
collection.load()

# # 1,64
# what is wrong? wtf?
# queryData = queryData.tolist()
results = collection.search(
    data=[queryData],  # this is the float dimension.
    anns_field="video_phash",
    param=search_params,
    output_fields=["video_length"],
    limit=10,
    expr="video_length > 1.2 and video_length < 4",
    # expr='video_length < 1.2',
)
theHit = results[0]
print(theHit)
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
