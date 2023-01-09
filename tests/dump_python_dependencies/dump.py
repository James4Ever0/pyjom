import datetime
log_dir = "logs"
now = datetime.datetime.now().isoformat().replace(".","_").replace(" ","_")

print('DUMP TIME:',now)

cmd = "pip3 list > {}/py3_deps_{}.log".format(log_dir,now)

import os
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

os.system(cmd)