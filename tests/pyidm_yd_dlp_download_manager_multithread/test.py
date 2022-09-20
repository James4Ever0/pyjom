url = "https://media3.giphy.com/media/wTrXRamYhQzsY/giphy.gif?cid=dda24d502m79hkss38jzsxteewhs4e3ocd3iqext2285a3cq&rid=giphy.gif&ct=g"

# import pyidm

from pySmartDL import SmartDL

url = "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"
dest = "C:\\Downloads\\" # or '~/Downloads/' on linux

obj = SmartDL(url, dest)
obj.start()
# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]

path = obj.get_dest()