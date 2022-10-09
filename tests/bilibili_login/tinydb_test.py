import tinydb

dbLocation = "test.json"
db = tinydb.TinyDB(dbLocation)
table = db.table('mytable')
table.upsert({'abc': 'def'}) # please specify a condition!