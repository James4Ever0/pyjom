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

db = SqliteDatabase("my_database.db") # this database exists in local filesystem.


class User(db.Model):
    username = CharField(unique=True)
    # what about let's modify this shit?


class Account(db.Model):
    user = ForeignKeyField(User)
    password = CharField() # you need to create a new table. do not modify this in place.
    # maybe you want tinydb or something else.

# User.bind(db) # this can dynamically change the database. maybe.
class User2(Model): # what is this model for? empty?
    username = CharField(unique=True)


# db.connect()``
# if using context manager, it will auto connect. no need to do shit.
db.create_tables([User, Account])

# charlie = User.create(username='charlie') # fail the unique check. will raise exception.
charlie, flag= User.get_or_create(username="charlie")  # will work without exception.
# print(charlie)
# breakpoint()
charlie_account, flag= Account.get_or_create(user = charlie, password='abcd') # this is not unique. warning!
print(charlie_account)
breakpoint()
# charlie = User.update(username='michael') # no insertion?
# use get_or_create here.
michael = User.get_or_create(username="michael")
# (data, flag)

data = User.get()  # this can only get one such instance?
# get one single instance, aka: first.
# print(data)
# breakpoint()

selection = User.select()  # still iterable?
# breakpoint()

# let's bind some database.
# User2.bind(db)
# if i don't bind the database what would happen?
# error!
# you need create such table first.
# User2.create_table()
db.create_tables([User2])

User2.get_or_create(username='abcdef')
print([x for x in User2.select()])