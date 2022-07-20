target_dir = "/media/root/help/pyjom/tests/wechat_bots/msimg32.dll_wechat_hook_webapi/docs/www.showdoc.com.cn/aixed"

import os

files = os.listdir(target_dir)

for fnames in files:
    filepath = os.path.join(target_dir, fnames)
    with open(filepath,"r",encoding="utf-8") as f:
        data = f.read()
    sites = ["host.indexOf('{}')".format(keyword) for keyword in ["localhost","127.0.0.1"]]
    target_site = "host.indexOf('{}')".format("dummy_site")
    for site in sites:
        data = data.replace(site, target_site)
    with open(filepath,"w",encoding="utf-8") as f: f.write(data)