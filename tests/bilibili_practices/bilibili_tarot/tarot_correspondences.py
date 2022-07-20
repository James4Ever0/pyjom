dirs =["tarot_pictures","tarot_pictures2"] 

import os
from tarot_descriptions import *

mtarget_0 = {k:None for k in mdict.keys()}
mtarget_1 = {k:None for k in smdict.keys()}

fn = []
for d in dirs:
    fnames = os.listdir(d)
    fnames = [os.path.join(d,f) for f in fnames]
    fn+= fnames
popdict = []
for k in mtarget_0.keys():
    if k == 0:
        kv = "0"
    else:
        kv = int_to_Roman(k)
    for f in fn:
        fb = os.path.basename(f)
        f0 = fb.split(".")[0].split("_")[0]
        if f0.upper() == kv:
            mtarget_0[k] = f
            break
    if mtarget_0[k] is None:
        popdict.append(k)
for k in popdict:
    mtarget_0.pop(k)

popdict = []

for k in mtarget_1.keys():
    kv =  smdict2[k]
    for f in fn:
        fb = os.path.basename(f)
        f0 = fb.split(".")[0].split("_")[-1]
        if kv.upper() in f0.upper():
            mtarget_1[k] = f
            break
    if mtarget_1[k] is None:
        popdict.append(k)
for k in popdict:
    mtarget_1.pop(k)

# print()
# ########printing.
# pretty good.
# if __name__ == "__main__":
#     for k in mtarget_0.keys():
#         print("MAJOR",k,mtarget_0[k])
#     for k in mtarget_1.keys():
#         print("MINOR",k,mtarget_1[k])