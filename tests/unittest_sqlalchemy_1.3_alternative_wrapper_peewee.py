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

db = SqliteDatabase("my_database.db")  # this database exists in local filesystem.


class User(db.Model):
    username = CharField(unique=True)
    # what about let's modify this shit?


class Account(db.Model):
    # charlie_account.user_id to get username?
    user = ForeignKeyField(User)  # what is this??
    # if you don't set field, the user_id will be the default User.id
    # user = ForeignKeyField(User, field=User.username) # what is this??
    password = (
        CharField()
    )  # you need to create a new table. do not modify this in place.
    # maybe you want tinydb or something else.


# User.bind(db) # this can dynamically change the database. maybe.
class User2(Model):  # what is this model for? empty?
    username = CharField(unique=True)


import datetime


class BilibiliVideo(db.Model):
    bvid = CharField(unique=True)
    visible = BooleanField()
    last_check = DateTimeField(
        default=datetime.datetime.now
    )  # this is default callable. will be managed as expected
    # poster = ForeignKeyField(User) # is it my account anyway?


# db.connect()
# if using context manager, it will auto connect. no need to do shit.
# are you sure you want to comment out the db.connect?
# actually no need to connect this. it will auto connect.
db.create_tables(
    [User, Account, BilibiliVideo]
)  # it is the same damn database. but shit has happened already.
# it is the foreign key reference.

# charlie = User.create(username='charlie') # fail the unique check. will raise exception.
charlie, flag = User.get_or_create(username="charlie")  # will work without exception.
# print(charlie)
# breakpoint()

# why we can pass a function instead of the object?
# last_check = datetime.datetime.now()

video_record, flag = BilibiliVideo.get_or_create(bvid="BV123", visible=False)

# print(video_record) # it will be good.
# breakpoint()

next_check_time = datetime.datetime.now() - datetime.timedelta(
    minutes=20
)  # every 20 minutes check these things.

# but for those which are already recognized as visible, we may not want to check these video till we select/search them. this is to reserve bandwidth.

print("NEXT CHECK TIME:", next_check_time)

results_0 = BilibiliVideo.select().where(
    BilibiliVideo.last_check < datetime.datetime.now()
)  # needs to check
results_1 = BilibiliVideo.select().where(
    BilibiliVideo.last_check > datetime.datetime.now()
)  # no need to check

print(results_0)
print(results_1)  # these are just raw sql statements. have't executed yet.
breakpoint()

# warning: our table name is lowercased. may cause trouble.
# but many sql statements are lower cased. case insensitive. at least my data are not case insensitive.

charlie_account, flag = Account.get_or_create(
    user=charlie, password="abcd"
)  # this is not unique. warning!
print(charlie_account)
# breakpoint()
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

User2.get_or_create(username="abcdef")
print([x for x in User2.select()])

username = "nonexistant"
# try:
answer = User2.get_or_none(User2.username == username)  # still raise exception huh?
print("ANSWER:", answer)  # great this is simpler.
if answer is None:
    print("username does not exist:", username)
# except Exception as e:
#     # print('exception type:', type(e))
#     print('username does not exist:', username)
#     # exception type: <class '__main__.User2DoesNotExist'>
