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

# some patch on /usr/local/lib/python3.9/dist-packages/peewee.py:3142

# is it just a single file? no other files?
# @property
# def Model(self): # this is interesting. does it work as expected?
#     class BaseModel(Model):
#         class Meta:
#             database = self
#     return BaseModel

db = SqliteDatabase('my_database.db')


class User(BaseModel):
    username = CharField(unique=True)