# are you sensitive to return?

# you can first replace the code with the 
cat test.py | comby ':[prefix~(@.+)*$]def :[functionName](:[args]):'  ':[prefix] @reloading def :[functionName](:[args]):' -stdin -stdout -matcher .py 