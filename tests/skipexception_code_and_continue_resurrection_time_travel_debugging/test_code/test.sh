# are you sensitive to return?

# you can first replace the code with the selected 
cat test.py | comby ':[prefix~(@.+)*$]def :[functionName](:[args]):'  ':[prefix] @reloading def :[functionName](:[args]):' -rule 'where match :[prefix] { |:[@someRandomDecorator] -> true | } '-stdin -stdout -matcher .py 