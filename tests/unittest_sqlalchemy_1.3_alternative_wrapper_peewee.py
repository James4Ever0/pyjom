# now we try to create and persist a database.

# do not delete it. we will check again.

# the data we put into are some timestamps.

# some peewee by the same guy who developed some database.

# https://github.com/coleifer/peewee

# 1.3.24 original sqlalchemy version, for our dearly chatterbot.

# currently: 1.4.42
# warning! might be incompatible.

from peewee import *
import datetime


db = SqliteDatabase('my_database.db')
db.