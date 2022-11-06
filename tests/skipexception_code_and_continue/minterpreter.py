# shall the code share modified version of statements?

source_code = open('test.py', 'r').readlines()

for line in source_code:
    indentLevel = len(line.replace(line.strip(),""))/4
    print(line, indentLevel)