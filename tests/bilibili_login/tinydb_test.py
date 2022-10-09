import tinydb

dbLocation = "test.json"
db = tinydb.TinyDB(dbLocation)
db.upsert({'abc': 'def'})