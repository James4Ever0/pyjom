# are you sensitive to return?
cat test.py | comby ':[prefix~$]def :[functionName](:[args]):'  ':[prefix]:[~\n]@reloading def :[functionName](:[args]):' .py  -matcher .py 