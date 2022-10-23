# now we try to create and persist a database.

# do not delete it. we will check again.

# the data we put into are some timestamps.

# some peewee by the same guy who developed some database.

# https://github.com/coleifer/peewee

# 1.3.24 original sqlalchemy version, for our dearly chatterbot.

# currently: 1.4.42
# warning! might be incompatible.

from peewee import *

# some patch on /usr/local/lib/python3.9/dist-packages/peewee.py:3142

# is it just a single file? no other files?
# @property
# def Model(self): # this is interesting. does it work as expected?
#     class BaseModel(Model):
#         class Meta:
#             database = self
#     return BaseModel

db = SqliteDatabase("my_database.db")


class User(db.Model):
    username = CharField(unique=True)

# User.bind(db) # this can dynamically change the database. maybe.
class User2(Model): # what is this model for? empty?
    username = CharField(unique=True)


# db.connect()``
# if using context manager, it will auto connect. no need to do shit.
db.create_tables([User])

# charlie = User.create(username='charlie') # fail the unique check. will raise exception.
charlie = User.update(username="charlie")  # will work without exception.
# charlie = User.update(username='michael') # no insertion?
# use get_or_create here.
michael = User.get_or_create(username="michael")
# (data, flag)

data = User.get()  # this can only get one such instance?
# get one single instance, aka: first.
# print(data)
# breakpoint()

selection = User.select()  # still iterable?
breakpoint()
