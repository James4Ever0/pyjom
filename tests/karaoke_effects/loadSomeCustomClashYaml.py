import yaml


# yaml.add_constructor(mCustomLoaderTag, create_ref, Loader)
def goYamlToPyYaml(docString):
    docString = docString.replace("!<str>", "!!str")
    return docString


def pyYamlToGoYaml(docString):
    docString = docString.replace("!!str", "!<str>")
    return docString


if __name__ == "__main__":

    fileName = "Clash.yaml"

    docString = open(fileName, "r").read()

    mCustomLoaderTag = "!<str>"

    class Ref(object):
        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return '"%s"' % self.data

    def create_ref(loader, node):
        # print(dir(loader))
        # breakpoint()
        value = loader.costruct_string(node)
        return Ref(value)

    class Loader(yaml.SafeLoader):
        pass

    docString = goYamlToPyYaml(docString)
    a = yaml.load(docString)
    print(a)
