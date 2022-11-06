# shall the code share modified version of statements?

source_code = open('test.py', 'r').readlines()

for line in source_code:
    indentLevel = int(len(line.replace(line.strip(),"").replace('\n',''))/4)
    print(line, indentLevel)
    if line.startswith('')