t=open("/root/Desktop/works/pyjom/pyjom/platforms/bilibili/postMetadata.py","r").read()

import redbaron
from create_decnode import getd

r=redbaron.RedBaron(t)

for n in r:
    print("name",n.name)
    n.help()
    flag=type(n)==redbaron.DefNode
    print("is defnode?",flag)
    if flag:
        print("is async?",n.async_)
        #print("is async?",n.__dict__["async"])
        print("decorators")
        print(type(n.decorators))
        #n.decorators.append(getd())
        # use official method instead.
        n.decorators.append("@offdec")
        for d in n.decorators:
            dt=type(d)
            isdt = dt == redbaron.DecoratorNode
            print("is decorator?",isdt)
    print("node")
    print(n)
    print(dir(n))

print("----")
print(r.dumps())
