# are you sensitive to return?
cat test.py | comby ':[[prefix]]def :[functionName](:[args]):' 'where :[prefix] == ""' .py -match-only -matcher .py