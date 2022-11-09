c=open("test2.py","r").read()

import pasta

tree=pasta.parse(c)
print(dir(tree))
f=tree.body[0]
print(dir(f))
dec = f.decorator_list
print(dec)
#c0=pasta.dump(tree)
print(dec[1].id) # now this is not a name object. it is a call object.
#print(c0)
