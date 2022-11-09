import pasta
import ast


tree=pasta.parse(c)
# print(dir(tree))
for i in range(len(tree)):
    f = tree.body[i]
    # f=tree.body[0]
    # print(dir(f))
    # del f.decorator_list[0]
    # f.decorator_list.append(ast.Name('newdec')) #seems good?
    # ast.FunctionDef and ast.AsyncFunctionDef are different.
    dec = f.decorator_list
    # print(dec)
    c0=pasta.dump(tree)
    # print(dec[1].id) # now this is not a name object. it is a call object.
    # print("___")
    # print(c0)
    # ast.FunctionDef 

if __name__ == "__main__":
    c=open("test2.py","r").read()