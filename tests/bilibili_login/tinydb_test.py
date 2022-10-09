import tinydb

dbLocation = "test.json"
db = tinydb.TinyDB(dbLocation)
table = db.table('mytable')
User = db.Q
table.upsert({'abc': 'def', 'ghi': 123}, User.ghi == 123) # please specify a condition!