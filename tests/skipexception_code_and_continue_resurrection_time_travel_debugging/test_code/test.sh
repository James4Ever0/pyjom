# are you sensitive to return?
cat test.py | comby ':[prefix~$]def :[functionName](:[args]):'  .py -match-only -matcher .py