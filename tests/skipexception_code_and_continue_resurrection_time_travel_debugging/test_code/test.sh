# are you sensitive to return?
cat test.py | comby ':[prefix~$]def :[functionName](:[args]):'  ':[functionName]' .py  -matcher .py