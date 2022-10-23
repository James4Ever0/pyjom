# now we try to create and persist a database.

# do not delete it. we will check again.

# the data we put into are some timestamps.

from sqlalchemy import Column, ForeignKey, Integer, String

# there are some tutorials on this.

from sqlalchemy import create_engine

dbpath = "test_sqlalchemy.db"

engine = create_engine('sqlite:///{}'.format(dbpath)) # where are you going to store this shit?