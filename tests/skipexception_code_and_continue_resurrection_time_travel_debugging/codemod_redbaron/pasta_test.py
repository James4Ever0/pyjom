import pasta
import ast


def recover_and_rewrite(c):
    c = c.replace("from reloading import reloading\n","")
    c = "from reloading import reloading\n"+c
    tree=pasta.parse(c)
    # print(dir(tree))
    for i in range(len(tree.body)):
        f = tree.body[i]
        if type(f) == ast.FunctionDef:
            removeList = []
            for index, elem in enumerate(f.decorator_list):
                if type(elem) == ast.Name:
                    if elem.id == 'reloading':
                        removeList.append(index)
            for index in removeList:
                del f.decorator_list[index]
            f.decorator_list.append(ast.Name('reloading')) #seems good?
        # ast.FunctionDef and ast.AsyncFunctionDef are different.
    c0=pasta.dump(tree)
    return c0

if __name__ == "__main__":
    c=open("test2.py","r").read()
    c0 = recover_and_rewrite(c)
    print(c0)