# shall the code share modified version of statements?

source_code = open('test.py', 'r').readlines()

for line in source_code:
    line=line.replace('\n','')
    indentLevel = int(len(line.replace(line.strip(),""))/4)
    print(line, indentLevel)
    if line.startswith('def '):
        # wrap with some decorator!
        # do not modify too much. the decorator is recursive so every function will be analyzed. is it?