import pasta
import ast


def recover_and_rewrite(c,no_rewrite=False):
    c = c.replace("from reloading import reloading\n", "")
    if not no_rewrite:
        c = "from reloading import reloading\n" + c
    tree = pasta.parse(c)
    # print(dir(tree))
    for i in range(len(tree.body)):
        f = tree.body[i]
        if type(f) == ast.FunctionDef:
            cached = False
            removeList = []
            for index, elem in enumerate(f.decorator_list):
                if type(elem) == ast.Name:
                    if elem.id == "reloading":
                        removeList.append(index)
                    elif "lru_cache" in elem.id: # are you sure you won't call that again?
                        cached = True
                elif type(elem) == ast.Call:
                    # breakpoint()
                    if type(elem.func) == ast.Name:
                        if "lru_cache" in elem.func.id:
                            cached = True
            for index in removeList:
                del f.decorator_list[index]
            # if len(f.decorator_list) == 0: # are you sure this will be ok?
            if not no_rewrite:
                if not cached:
                    f.decorator_list.append(ast.Name("reloading"))  # seems good?
        # ast.FunctionDef and ast.AsyncFunctionDef are different.
    c0 = pasta.dump(tree)
    return c0


if __name__ == "__main__":
    c = open("test2.py", "r").read()
    c0 = recover_and_rewrite(c)
    print(c0)
