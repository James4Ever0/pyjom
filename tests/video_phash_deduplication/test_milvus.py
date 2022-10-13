# duplicate -> remove, do not insert
# not duplicate -> get the data, insert

# you want to clear the collection after this run?

# import pymilvus
from pymilvus import connections

connection = connections.connect(alias="default", host="localhost", port="19530")
collection_name = "video_deduplication"


from pymilvus import Collection

# Collection(collection_name)
# remote this thing.
from pymilvus import utility

try:
    utility.drop_collection(collection_name)
except:
    import traceback
    traceback.print_exc()
    print("maybe the collection does not exist")

from pymilvus import CollectionSchema, FieldSchema, DataType

video_semantic_id = FieldSchema(
    name="video_semantic_id",
    dtype=DataType.INT64,
    is_primary=True,
)
video_length = FieldSchema(
    name="video_length",
    dtype=DataType.FLOAT,
)
video_phash = FieldSchema(name="video_phash", dtype=DataType.BINARY_VECTOR, dim=64)  # 64
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
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
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
queryData = queryData.tobytes()
# dimension: 8*8=64
collection.insert([[1], [np.float32(3.5)], [queryData]])
# print(len(queryData), len(queryData)*8)
# # print(queryData.shape)
# breakpoint()
collection.load()
collection.

# # 1,64
# what is wrong? wtf?
# queryData = queryData.tolist()
results = collection.search(
    data=[queryData],  # this is the float dimension.
    anns_field="video_phash",
    param=search_params,
    limit=10,
    expr=None,
    consistency_level="Strong",
)
print(results)
