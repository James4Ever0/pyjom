import tinydb

dbLocation = "test.json"
db = tinydb.TinyDB(dbLocation)
table = db.table('mytable')
table.upsert({'abc': 'def', 'ghi'}) # please specify a condition!