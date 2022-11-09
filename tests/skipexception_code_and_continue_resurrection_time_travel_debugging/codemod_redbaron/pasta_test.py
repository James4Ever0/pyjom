c=open("test2.py","r").read()

import pasta

tree=pasta.parse(c)
print(dir(tree))
f=tree.body[0]
print(dir(f))
print(f.decorator_list)
#c0=pasta.dump(tree)

#print(c0)
