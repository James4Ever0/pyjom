import bowler

src ='test2.py'

pattern="""

"""

q = bowler.Query(src)
f = q.select(pattern)
print(f)