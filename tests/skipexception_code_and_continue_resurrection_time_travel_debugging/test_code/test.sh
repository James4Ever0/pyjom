# are you sensitive to return?
cat test.py | comby ':[prefix~$]def :[functionName](:[args]):'  ':[prefix]:[functionName]' .py  -matcher .py