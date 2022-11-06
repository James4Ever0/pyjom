# shall the code share modified version of statements?

source_code = open('test.py', 'r').readlines()

for line in source_code:
    line=line.replace('\n','')
    indentLevel = int(len(line.replace(line.strip(),""))/4)
    if line == "": continue
    print((indentLevel*2)*4*" "+'try:')
    print((indentLevel*2+1)*4*" "+line, "[{}]".format(indentLevel))
    if line.startswith("def "): continue
    print((indentLevel*2)*4*" "+'except: pass')