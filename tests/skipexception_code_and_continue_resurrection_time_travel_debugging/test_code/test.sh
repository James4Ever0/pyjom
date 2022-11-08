# are you sensitive to return?
cat test.py | comby ':[prefix~$]def :[functionName](:[args]):'  ':[prefix]def :[functionName]' .py  -matcher .py