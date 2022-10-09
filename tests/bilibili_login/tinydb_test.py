import tinydb

dbLocation = "test_credential.json"
db = tinydb.TinyDB(dbLocation)
# table = db.table('mytable')
User = tinydb.Query()
db.upsert({"abc": "def", "ghi": 123}, User.ghi == 123)  # please specify a condition!
# db.update({'abc': 'def', 'ghi': 123}) # no insert here!
