# shall the code share modified version of statements?

source_code = open('test.py', 'r').readlines()

registeredLevels = []
for line in source_code:
    line=line.replace('\n','')
    indentLevel = int(len(line.replace(line.strip(),""))/4)
    if len(registeredLevels)>0 and indentLevel< registeredLevels[-1]:
    print((indentLevel*2)*4*" "+'except: pass')


    if line == "": continue
    print((indentLevel*2)*4*" "+'try:')
    print((indentLevel*2+1)*4*" "+line, "[{}]".format(indentLevel))
    if line.startswith("def "):
        unclosedTryExceptCounts+=1
        registeredLevels.append(indentLevel)
        continue
    print((indentLevel*2)*4*" "+'except: pass')