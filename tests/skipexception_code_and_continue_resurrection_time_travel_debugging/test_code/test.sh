# are you sensitive to return?
cat test.py | comby ':[\n]def :[functionName](:[args]):' .py -match-only -matcher .py