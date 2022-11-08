from comby import Comby

comby = Comby()
source_old = open('new_test.py','r').read()
kw = 'from reloading import reloading\n'
source_old = source_old.replace(kw,"") # obliterate this thing.

match = ':[prefix~@reloading.*$]def :[functionName](:[args]):'
rewrite = 'def :[functionName](:[args]):'

source_new = comby.rewrite(source_old, match, rewrite)

print(source_new)