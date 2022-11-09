c=open("test2.py","r").read()

import pasta

tree=pasta.parse(c)
c0=pasta.dump(tree)

print(c0)
