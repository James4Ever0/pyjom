url = "https://media3.giphy.com/media/wTrXRamYhQzsY/giphy.gif?cid=dda24d502m79hkss38jzsxteewhs4e3ocd3iqext2285a3cq&rid=giphy.gif&ct=g"

# import pyidm

from pySmartDL import SmartDL

dest = "./test.gif"
obj = SmartDL(url, dest)
obj.start()
# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]
print('DOWNLOAD FINISHED')
path = obj.get_dest()
print("DOWNLOADED AT:", path)