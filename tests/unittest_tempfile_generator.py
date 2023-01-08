import tempfile


def generateFile():
    data = b"abc"
    while True:
        with tempfile.NamedTemporaryFile("wb", suffix=".data") as f:
            name = f.name
            print("tempfile name:", name)
            f.write(data)
            f.seek(0)  # strange.
            # what the fuck?
            # f.close()
            yield name


if __name__ == "__main__":
    grt = generateFile()
    filepath = grt.__next__()
    for _ in range(2):
        # good?
        with open(filepath, "rb") as f:
            content = f.read()
            print("content in {}:".format(filepath), content)
