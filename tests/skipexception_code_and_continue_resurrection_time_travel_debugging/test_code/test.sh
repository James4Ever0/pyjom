# are you sensitive to return?

# you can first replace the code with the selected 

# cat new_test.py | comby ':[prefix~@reloading.*$]def :[functionName](:[args]):'  'def :[functionName](:[args]):' -stdin -stdout -matcher .py |  comby "from reloading import reloading"  '' -stdin -stdout -matcher .py 

# cat test.py | comby ':[prefix~(@.+)*$]def :[functionName](:[args]):'  ':[prefix] @reloading def :[functionName](:[args]):' -rule 'where match :[prefix] { | :[_@someRandomDecorator.*] -> true | :[_] -> false } ' -stdin -stdout -matcher .py -match-only

cat /root/Desktop/works/pyjom/pyjom/platforms/bilibili/utils.py | comby ':[prefix~(@.+)*$]def :[functionName](:[args]):'  ':[prefix] @reloading def :[functionName](:[args]):' -stdin -stdout -matcher .py -match-only