# shall the code share modified version of statements?

source_code = open("test.py", "r").readlines()

registeredLevels = []
# should use restorable arrays/dict.
for lineNumber, line in enumerate(source_code):
    line = line.replace("\n", "")
    indentLevel = int(len(line.replace(line.strip(), "")) / 4)
    # print(registeredLevels)
    exceptCodes = ["print('exception on code line: {}')".format(lineNumber)]
    if len(registeredLevels) > 0 and indentLevel <= registeredLevels[-1]:
        mIndentLevel = registeredLevels.pop(-1)
        print((mIndentLevel * 2) * 4 * " " + "except:")
        for exceptCode in exceptCodes:
            print((mIndentLevel * 2+1) * 4 * " " +exceptCode)
    if line == "":
        continue
    print((indentLevel * 2) * 4 * " " + "try:")
    print((indentLevel * 2 + 1) * 4 * " " + "print('entering code line: {}')".format(lineNumber))
    line=line.strip()
    # if not line.startswith('return '):
    print((indentLevel * 2 + 1) * 4 * " " + line, "# indent[{}]".format(indentLevel))
    if line.startswith("def "):
        registeredLevels.append(indentLevel)
        continue
    print((indentLevel * 2) * 4 * " " + 'except:')
    for exceptCode in exceptCodes:
        print((indentLevel * 2+1) * 4 * " " + exceptCode)
