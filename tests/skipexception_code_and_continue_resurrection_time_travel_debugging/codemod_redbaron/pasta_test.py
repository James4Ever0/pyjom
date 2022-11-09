import pasta
import ast


tree=pasta.parse(c)
# print(dir(tree))
for i in range(len(tree)):
    f = tree.body[i]
    if type(f) == ast.FunctionDef:
        removeList = []
        for index, elem in f.decorator_list:
            if type(elem) == ast.Name:
                if elem.id == 'reloading':
                    removeList.append(index)
        for index in removeList:
            del f.decorator_list[index]
        f.decorator_list.append(ast.Name('reloading')) #seems good?
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