import bowler

src ='test2.py'

q = bowler.Query(src)
f = q.select_function()
print(f)