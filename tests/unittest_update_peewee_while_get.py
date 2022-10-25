dbpath = 'test.db'

from peewee import *

class BilibiliUser(Model):
    username = CharField()
    user_id = IntegerField(unique=True)
    is_mine = BooleanField(default=False)
    followers = IntegerField(
        null=True
    )  # how to get that? every time you get some video you do this shit? will get you blocked.
    # well you can check it later.
    avatar = CharField(null=True)  # warning! charfield max length is 255

db=SqliteDatabase(dbpath)
db.create_tables(BilibiliUser)

BilibiliUser.get_and_update_or_create(username=username, user_id=1,is_mine=False, )