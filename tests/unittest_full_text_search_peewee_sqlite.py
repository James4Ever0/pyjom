from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, FTSModel, SearchField, RowIDField

db_path = "test_fulltext_search.db"

db = SqliteExtDatabase(
    db_path, pragmas={"journal_mode": "wal", "cache_size": -1024 * 64}
)


class BilibiliVideoIndex(FTSModel):
    rowid = RowIDField()  # this does not support
    title = SearchField()
    content = SearchField()

    class Meta:
        database = None  # that's good.
        options = {"tokenize": "porter"}  # you need manually separate some


db.create_tables([BilibiliVideoIndex])

import uuid

randomContent = lambda: str(uuid.uuid4())

object, flag = BilibiliVideoIndex.get_and_update_or_create(
    rowid=1, title=randomContent(), content=randomContent(), _unique_keys=["rowid"]
)


BilibiliVideoIndex.get_and_update_or_create(
    rowid=2,
    title="hello world",
    content="learn python the hard way",
    _unique_keys=["rowid"],
)
BilibiliVideoIndex.get_and_update_or_create(
    rowid=3,
    title="hello world",
    content="learn python the hard way",
    _unique_keys=["rowid"],
)
BilibiliVideoIndex.get_and_update_or_create(
    rowid=4,
    title="hello world",
    content="learn python the hard way",
    _unique_keys=["rowid"],
)
print(object)
print(flag)

print(object.rowid, object.title, object.content)

# don't know what magic is inside. whatever.

# updated. my lord.
# now search for it.

term = "python world"
results = BilibiliVideoIndex.search_bm25(term).limit(2)  # just how many?
# breakpoint()
# it does have the limit.

# it is ordered.
for result in results:
    print("RESULT", result)
    breakpoint()
