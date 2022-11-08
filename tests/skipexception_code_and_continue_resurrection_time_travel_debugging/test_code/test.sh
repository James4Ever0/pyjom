# are you sensitive to return?
cat test.py | comby ':[prefix~$]def :[functionName](:[args]):'  ':[prefix]@reloading\ndef :[functionName]' .py  -matcher .py