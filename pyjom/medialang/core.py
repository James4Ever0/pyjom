from pyjom.commons import *
from pyjom.medialang.commons import *
from pyjom.medialang.processors import *
import re
import traceback


class lexicalItem:
    def __init__(self, path, **kwargs):
        self.path = path
        self.args = kwargs
        self.indent = 0
        self.index = 0

    def __repr__(self):
        indent = "    " * self.indent
        mRepr = []
        mRepr.append("{}___medialang_item_[{}]".format(indent, self.index))
        mRepr.append("{}item path:".format(indent)+"  "+ self.path)
        mRepr.append("{}item args:".format(indent)+"  "+ str(self.args))
        return "\n".join(mRepr) # is this magic?


class lexicalGroup:
    def __init__(self, items=[]):
        self.items = []
        self.index = 0
        self.indent = 0
        for item in items:
            assert type(item) == lexicalItem
            self.items.append(item)

    def append(self, item):
        assert type(item) == lexicalItem
        self.items.append(item)

    def dump(self):
        for item in self.items:
            yield item # you yield NONE? WTF?

    def __repr__(self):
        indent = "    " * self.indent
        mRepr = []
        mRepr.append("{}____________medialang_line_[{}]".format(indent, self.index))
        # print("ITEMS:", self.items)
        for i, item in enumerate(self.dump()):
            item.indent = self.indent + 1
            item.index = i
            mRepr.append(item)
        # should we return nothing?
        return "\n".join(mRepr)


class lexicalScript:
    def __init__(self, lines=[]):
        self.lines = []
        self.indent = 0
        self.index = 0
        for line in lines:
            assert type(line) == lexicalGroup
            self.lines.append(line)

    def append(self, line):
        assert type(line) == lexicalGroup
        self.lines.append(line)

    def dump(self):
        for line in self.lines:
            yield line

    def __repr__(self):
        indent = "    " * self.indent
        mRepr = []
        mRepr.append("{}____________medialang_script_[{}]".format(indent, self.index))
        for i, item in enumerate(self.dump()):
            item.indent = self.indent + 1
            item.index = i
            mRepr.append(item)
        return "\n".join(mRepr)

class Medialang:
    def __init__(
        self,
        script_path=None,
        script=None,
        script_obj=None,
        encoding="utf-8",
        indent=4,
        template=False,
        template_args={},
        verbose=True,
        medialangTmpdir=medialangTmpDir
    ):
        self.verbose = verbose
        self.medialangTmpDir = medialangTmpDir
        self.indent = " " * indent
        self.script_path = script_path
        self.script_obj = script_obj
        self.script = script
        self.encoding = encoding
        lexList = [script_path, script, script_obj]
        lexCheck = sum([int(x is None) for x in lexList]) == 2
        if not lexCheck:
            raise Exception(
                "Can only pass one value to either of script_path, script, script_obj:\n{}".format(
                    lexList
                )
            )
        if script_path is None:
            if script is None:
                assert script_obj is not None
                assert template is False
                self.script_obj = script_obj
            else:
                assert type(script) == str
                self.script = script

        else:
            assert type(script_path) == str
            try:
                abspath = getAbsoluteFilePath(script_path)
            except:
                medialangFatalError(
                    "Failed to resolve script path: {}".format(script_path), __file__
                )
            self.script_path = abspath
            extension = getFileExtension(script_path)
            if template:
                assert extension == "j2"
            else:
                assert extension in ["mdl", "media"]
            with open(abspath, "r", encoding=encoding) as f:
                self.script = f.read()
        if self.script_obj is not None:
            self.script = self.generate(self.script_obj)
        else:
            if template:
                assert type(template_args) == dict
                self.script = renderTemplate(self.script, template_args)
            self.script_obj = self.parse(self.script)

    def generate_item(self, item_obj, line_max_char=40, level=0):
        # content = item_obj.content
        path = item_obj.path
        item_lines = ['"{}"'.format(path)]
        # print("item_lines:",item_lines)
        args = item_obj.args
        # print("path:",path)
        for key in args.keys():
            assert not key.startswith("#")
            # print("key:",key)
            mitem = args[key]
            if type(mitem) is str:
                mitem = '"{}"'.format(mitem)
            elif type(mitem) in [float, int]:
                mitem = str(mitem)
            elif mitem in [True, False]:
                mitem = str(mitem).lower()
            else:
                mitem_trial = json.dumps(mitem)
                if len(mitem_trial) < line_max_char:
                    mitem = mitem_trial
                else:
                    mitem = json.dumps(mitem, indent=self.indent)
            mitem = "{}={}".format(key, mitem)
            mitem = mitem.split("\n")
            for mitem0 in mitem:
                trial_item = ", ".join([item_lines[-1], mitem0])
                if len(trial_item) < line_max_char:
                    item_lines[-1] = trial_item
                else:
                    item_lines.append(mitem0)
        item_lines = ",\n{}".format((1 + level) * self.indent).join(item_lines)
        # print("item_lines:",item_lines)
        item_lines = "{}({}\n{})\n".format(
            level * self.indent, item_lines, level * self.indent
        )
        item_lines = item_lines.replace(",,", ",")
        item_lines = item_lines.replace("[,", "[")
        item_lines = item_lines.replace(", }", "}")
        item_lines = item_lines.replace(", ]", "]")
        item_lines = item_lines.replace("{,", "{")
        return item_lines

    def generate(self, script_obj):
        # default prettify the target
        script = ""
        for line_obj in script_obj.dump():
            for level, item_obj in enumerate(line_obj.dump()):
                unit = self.generate_item(item_obj, level=level)
                # print("unit:",unit)
                script += unit
            script += "\n"

        script = script.replace(",,", ",")
        script = script.replace("[,", "[")
        script = script.replace(", }", "}")
        script = script.replace(", ]", "]")
        script = script.replace("{,", "{")
        i = 0
        maxIndent = 0
        # script = script.replace("'",'"') # no freaking single quotes.
        while True:
            if i == 0:
                script = script.replace(",\n]", "\n]")
                script = script.replace(",\n]", "\n]")
            else:
                indentStr = self.indent * i
                if indentStr in script:
                    script = script.replace(
                        ",\n{}]".format(indentStr), "\n{}]".format(indentStr)
                    )
                    script = script.replace(
                        ",\n{}".format(indentStr) + "}", "\n{}".format(indentStr) + "}"
                    )
                else:
                    maxIndent = i - 1
                    break
            i += 1
        for index0 in range(maxIndent):
            indentStr = self.indent * (maxIndent - index0)
            if indentStr in script:
                script = script.replace(
                    "{}], ".format(indentStr),
                    "{}],\n{}".format(indentStr, indentStr),
                )
                script = script.replace(
                    "{}".format(indentStr) + "}, ",
                    "{}".format(indentStr) + "},\n" + "{}".format(indentStr),
                )
        for index in range(maxIndent):
            indentStr = self.indent * (maxIndent - index)
            if indentStr in script:
                # print("running", len(indentStr))
                script = script.replace(
                    "[{}".format(indentStr),
                    "[",
                )
                script = script.replace(
                    ",{}".format(indentStr),
                    ",",
                )
                script = script.replace(
                    "{" + "{}".format(indentStr),
                    "{",
                )
        script = script.replace(",,", ",")
        script = script.replace("[,", "[")
        script = script.replace(", }", "}")
        script = script.replace(", ]", "]")
        script = script.replace("{,", "{")
        script = script.replace("{ {", "{{")
        script = script.replace("} }", "}}")
        script = script.replace("] ]", "]]")
        script = script.replace("[ [", "[[")
        script = script.replace("[ ", "[")
        if script.endswith("\n\n"):
            script = script[:-2]
        if script.startswith("\n"):
            script = script[1:]
        return script

    def detectGrammar(self, line):
        result = line.replace("\n", "").replace(" ", "").replace("\t", "")
        return len(result) != 0

    def getItems(self, line):
        # assume there will not be enclosed brackets in string?
        values = {"(": +1, ")": -1}
        base = 0
        items = []
        item = ""
        for char in line:
            value = 0 if char not in values.keys() else values[char]
            base += value
            if base > 0:
                item += char
            if base == 0 and value != 0:
                item += char
                items.append(item)
                item = ""
        return items

    def parseItem(self, item):
        # have dangerous eval.
        body = item.strip()
        body = item[1:-1]
        # print("body length:",len(body))
        path = re.findall(r'^"([^"]+)"', body)[0]
        # print("found path:",path)
        mdict = body[len(path) + 2 :]
        mdict = mdict.strip()
        if self.detectGrammar(mdict):
            mdict = mdict[1:]  # omit the comma.
            text = ""
            mdict2 = ""
            values = {"(": +1, ")": -1}
            base = 0
            try:
                assert mdict[-1] != ","
            except:
                raise Exception("Found trailing comma:\n", mdict)
            for index, char in enumerate(mdict):
                lineEnd = index == (len(mdict) - 1)
                value = 0 if char not in values.keys() else values[char]
                base += value
                if char == "=":
                    key = text.strip()
                    assert not key.startswith("#")
                    mdict2 += '"{}":'.format(key)
                    text = ""
                elif (char == "," and base == 0) or lineEnd:
                    if lineEnd:
                        text += char
                    mtext = text.strip()
                    # print("mtext:",mtext)
                    if mtext in ["False", "True"]:
                        mtext = mtext.lower()
                    mdict2 += "{}".format(mtext)
                    if not lineEnd:
                        mdict2 += ","
                    text = ""
                    if lineEnd:
                        break
                else:
                    text += char
            # print("mdict:",mdict)
            mdict2 = mdict2.replace("(", "[").replace(")", "]")
            mdict = "{" + mdict2 + "}"  # might be empty somehow.
            # print(mdict)
            mdict = json.loads(mdict)
        else:
            mdict = {}
        item_obj = lexicalItem(path, **mdict)
        return item_obj

    def parse(self, script):
        # will raise exception on unparseable lines.
        script_obj = lexicalScript()
        lines = script.split("\n\n")
        lines = [x for x in lines if self.detectGrammar(x)]
        for line in lines:
            line_obj = lexicalGroup()
            # first let's remove all comments.
            comment_expression = re.compile(r"#[^\n]+")
            newLine = ""
            for elem in comment_expression.split(line):
                if not comment_expression.match(elem):
                    newLine+=elem
            line = newLine
            line = line.replace("\n", "").replace("\t", "")
            line = line.strip()  # have extra spacings.
            for item in self.getItems(line):
                if self.detectGrammar(item):
                    # print("item:",item)
                    # print("item length:",len(item))
                    # breakpoint()
                    try:
                        item_obj = self.parseItem(item)
                        line_obj.append(item_obj)
                    except:
                        traceback.print_exc()
                        error_msg = "Error found in:\n{}".format(item)
                        if self.script_path:
                            error_msg += "\nScript at:\n{}".format(self.script_path)
                        raise Exception(error_msg)
            script_obj.append(line_obj)
        return script_obj

    def prettify(self, script=None, inplace=False):
        if script == None:
            assert self.script is not None
            script = self.script
        if self.script_obj is None:
            script_obj = self.parse(script)
        else:
            script_obj = self.script_obj
        script = self.generate(script_obj)
        if self.script_path is not None:
            if inplace:
                with open(self.script_path, "w+", encoding=self.encoding) as f:
                    f.write(script)
        return script

    def checkItemType(self, item):
        assert type(item) == lexicalItem  # you really should learn how to rest.
        path = item.path
        if path.startswith("."):
            return "output"
        for key in medialangProtocols:
            for elem in medialangProtocols[key]:
                if path.startswith(elem):
                    return key
        if os.path.exists(path):
            return "input"
        return "output"

    def objectAssertion(self, previous, objectType):
        assert objectType in ["input", "output"]
        if objectType == "output":
            assert previous is not None

    def objectExecutor(self, item, previous=None):
        objectType = self.checkItemType(item)
        path = item.path
        args = item.args
        self.objectAssertion(previous, objectType)
        result = {}  # how to ensure it will do?
        if objectType == "output":
            if path.startswith("."):
                function = dotProcessors[path]
                result = function(item, previous, verbose=self.verbose, medialangTmpDir=self.medialangTmpDir)
        else:
            if os.path.exists(path):
                data = fsProcessor(item, previous=previous, verbose=self.verbose, medialangTmpDir = self.medialangTmpDir)
                result = data
            else:
                pass
                # inputs. handle with protocols?
        return result

    def scriptStructExecutor(self, script_struct):
        script_type = script_struct["type"]
        resources = script_struct["resource"]
        targets = script_struct["target"]
        data_array = []
        data = None
        print("Medialang script type:", script_type)
        if script_type == "input":
            for item in targets.items:
                data = self.objectExecutor(item, previous=data)
            for resource in resources:
                mdata = copy.deepcopy(data)
                for item in resource.items:
                    mdata = self.objectExecutor(item, previous=mdata)
                data_array.append(mdata)
        else:
            for index0, resource in enumerate(resources):
                # print("RESOURCE ENUMERATE",index0, resource)
                # breakpoint()
                mdata = None
                mdata_array = []
                for index1, item in enumerate(resource.items):
                    mdata = self.objectExecutor(item, previous=mdata)
                    if self.verbose:
                        print("input {}-{}:".format(index0, index1), mdata) # this is the wrong data array!
                    mdata_array.append({"item":item, "cache": mdata}) # where you store all the intermediate files per clip.
                data_array.append(copy.deepcopy(mdata_array))
            data = copy.deepcopy(data_array) # so this is your freaking data! let's decide your approach all inside that dotProcessor instead of generating trash here!
            for item in targets.items:
                data = self.objectExecutor(item, previous=data)
        return data, data_array # why you return this!
        # currently, data is now the editly json, and data_array is the medialang items array
        # what about the slient flag? deal with it later!

    def execute(self):
        script_obj_lines = self.script_obj.lines
        assert len(script_obj_lines) >= 1
        script_struct = {
            "target": script_obj_lines[0],
            "resource": script_obj_lines[1:],
        }
        first_target = script_struct["target"].items[0]
        script_type = self.checkItemType(first_target)
        script_struct["type"] = script_type
        item_types = ["input", "output"]
        for item_type in item_types:
            if script_type == item_type:
                # this is analysis type mediascript. all following shall be output.
                for line in script_struct["resource"]:
                    elem = line.items[
                        0
                    ]  # only make sure the first item of each line is in agreement with the type rules.
                    this_item_type = self.checkItemType(elem)
                    try:
                        assert this_item_type is not item_type
                    except:
                        traceback.print_exc()
                        print("Medialang Error when parsing resource:")
                        print(line)
                        print("Medialang itemtype:", this_item_type)
                        print(elem)
                        if self.script_path:
                            print("Medialang Script path:", self.script_path)
                        os.abort()
                result = self.scriptStructExecutor(script_struct)
                return result  # tuple (data, data_array)
