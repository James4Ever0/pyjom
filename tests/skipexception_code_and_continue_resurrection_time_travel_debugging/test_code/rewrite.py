from comby import Comby

comby = Comby()
source_old = open('test.py','r').read()
match = ':[prefix~$]def :[functionName](:[args]):'
rewrite = ':[prefix]\n@reloading\ndef :[functionName](:[args]):'
source_new = comby.rewrite(source_old, match, rewrite)
# -> 'print("hello world")
source_new = 'from reloading import reloading\n'+source_new
print(source_new)