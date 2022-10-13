
# duplicate -> remove, do not insert
# not duplicate -> get the data, insert

# you want to clear the collection after this run?

# import pymilvus
from pymilvus import connections
connection = connections.connect(
  alias="default", 
  host='localhost', 
  port='19530'
)



from pymilvus import Collection

from pymilvus import CollectionSchema, FieldSchema, DataType
book_id = FieldSchema(
  name="video_semantic_id", 
  dtype=DataType.INT64, 
  is_primary=True, 
)
word_count = FieldSchema(
  name="video_length", 
  dtype=DataType.FLOAT,  
)
book_intro = FieldSchema(
  name="video_phash", 
  dtype=DataType.BINARY_VECTOR, 
  dim=2
)
schema = CollectionSchema(
  fields=[book_id, word_count, book_intro], 
  description="Test video deduplication"
)
collection_name = "video_deduplication"

# collection = Collection("video")      # Get an existing collection.
collection = Collection(
    name=collection_name, 
    schema=schema, 
    using='default', 
    shards_num=2,
    )
# is this demo collection?
collection.load()

# seems hard to setup.
# not started!
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

results = collection.search(
	data=[[0.1, 0.2]], 
	anns_field="video_phash", 
	param=search_params, 
	limit=10,
	expr=None,
	consistency_level="Strong"
)
