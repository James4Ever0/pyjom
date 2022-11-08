from comby import Comby

comby = Comby()
match = 'print :[[1]]'
rewrite = 'print(:[1])'
source_old = open('test.py','r').read()
source_new = comby.rewrite(source_old, match, rewrite)
# -> 'print("hello world")