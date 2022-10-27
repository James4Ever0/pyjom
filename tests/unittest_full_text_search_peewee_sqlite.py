from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, FTSModel

db_path = "test_fulltext_search.db"

db = SqliteExtDatabase(db_path, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})

class BilibiliVideoIndex(FTSModel):
    rowid = RowIDField()
    title = SearchField()
    content = SearchField()
    class Meta:
        database = db
        options = {'tokenize': 'porter'}

