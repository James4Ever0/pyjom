import pasta
import ast


def 
tree=pasta.parse(c)
# print(dir(tree))
for i in range(len(tree.body)):
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
c0=pasta.dump(tree)

if __name__ == "__main__":
    c=open("test2.py","r").read()