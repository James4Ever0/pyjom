
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
collection = Collection("video")      # Get an existing collection.

# is this demo collection?
collection.load()

# seems hard to setup.
# not started!
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

results = collection.search(
	data=[[0.1, 0.2]], 
	anns_field="book_intro", 
	param=search_params, 
	limit=10,
	expr=None,
	consistency_level="Strong"
)
