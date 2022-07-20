registry_key= "aiwxhook"

password = "YJI1E873652D6866A0C4B11481A43D7C" # some used password.

#password = "32DF76632DF766632DF766"

value_key = "卡密" # might be problem? unicode to gbk?

import winreg

string_type = winreg.REG_SZ

path = winreg.HKEY_LOCAL_MACHINE

def trypass(function):
    try: return function()
    except: pass

key = trypass(lambda: winreg.OpenKeyEx(path, r"SOFTWARE\\Wow6432Node"))
if not (key == None):
    newKey = trypass(lambda: winreg.CreateKey(key,registry_key))
    if not (key == None):
        trypass(lambda: winreg.SetValueEx(newKey,value_key,0,winreg.REG_SZ, password))
