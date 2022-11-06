# shall the code share modified version of statements?

source_code = open('test.py', 'r').readlines()

for line in source_code:
    indentLevel = [line.replace(line.strip().replace('\n'),"")]
    print(line, indentLevel)