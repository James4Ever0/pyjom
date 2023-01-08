dbpath = "test.db"

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


db = SqliteDatabase(dbpath)
db.create_tables([BilibiliUser])
import uuid

username = str(uuid.uuid4())

# u, _ = BilibiliUser.get_and_update_or_create(username=username, user_id=1)
BilibiliUser.update(username=username).where(BilibiliUser.user_id == 1).execute()
# why don't you update? need i delete it manually?

u = BilibiliUser.get(user_id=1)

print("current username:", username)
print("fetched username:", u.username)
