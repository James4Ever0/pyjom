from pyiqa.default_model_configs import DEFAULT_CONFIGS

mlist = []

for key in DEFAULT_CONFIGS.keys():
    config = DEFAULT_CONFIGS[key]
    mode = config["metric_mode"]
    if mode == "NR":
        mlist.append(key)

# print(mlist)
# forbid_lists = ["ilniqe","nima"]
allow_lists = ["niqe", "brisque", "paq2piq"]
for elem in mlist:
    if elem not in allow_lists:
        continue
    print(elem)

# i need to say these methods are not as useful as it was said.
# the objective shall be EMA based.

# ['niqe', 'ilniqe', 'brisque', 'nrqm', 'pi', 'musiq', 'musiq-ava', 'musiq-koniq', 'musiq-paq2piq', 'musiq-spaq', 'nima', 'paq2piq', 'dbcnn']
# you may try them all?

# it is really hard to say before we download all these models.
# seems not really dependent on the model size?

# we've got freaking huge shits.
# like this one, for nima.
# https://download.pytorch.org/models/vgg16-397923af.pth
# what is this shit for anyway?