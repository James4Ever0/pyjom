from comby import Comby

comby = Comby()


def recover(source_old):
    kws = ["from reloading import reloading", "@reloading"]
    # source_old = source_old.replace(kw,"") # obliterate this thing. shall we?
    source_old = "\n".join(
        [
            line
            for line in source_old.split("\n")
            if not any(line.startswith(elem) for elem in kws)
        ]
    )

    match = ":[prefix~@reloading.*$]def :[functionName](:[args]):"
    rewrite = "def :[functionName](:[args]):"

    source_new = comby.rewrite(source_old, match, rewrite, language=".py")
    return source_new


if __name__ == "__main__":
    # comby = Comby()

    source_old = open("new_test.py", "r").read()
    source_new = recover(source_old)
    print(source_new)
