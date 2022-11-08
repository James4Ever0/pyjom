from comby import Comby

comby = Comby()
match = ':[prefix~$]def :[functionName](:[args]):'
rewrite = ':[prefix]\n@reloading\ndef :[functionName](:[args]):'
source_old = open('test.py','r').read()
source_new = comby.rewrite(source_old, match, rewrite)
# -> 'print("hello world")
source_new = 'from rewrite import rewrite\n'+source_new
print(source_new)