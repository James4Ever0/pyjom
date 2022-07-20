# BaiduPCS-Go upload --norapid  --policy rsync externals/*.sh /pyjom/externals
# BaiduPCS-Go upload --norapid  --policy rsync externals/*.py /pyjom/externals
# BaiduPCS-Go upload --norapid  --policy rsync externals/*.log /pyjom/externals
# BaiduPCS-Go upload --norapid  --policy rsync logs /pyjom/
# BaiduPCS-Go upload --norapid  --policy rsync node_modules /pyjom/
# BaiduPCS-Go upload --norapid  --policy rsync pyjom /pyjom/
# BaiduPCS-Go upload --norapid  --policy rsync samples /pyjom/
# BaiduPCS-Go upload --norapid  --policy rsync tests /pyjom/
# BaiduPCS-Go upload --norapid  --policy rsync .gitignore /pyjom/
# BaiduPCS-Go upload --norapid  --policy rsync .git /pyjom/
# BaiduPCS-Go upload --norapid  --policy rsync *.* /pyjom/
BaiduPCS-Go upload --norapid  --policy rsync * /pyjom/
# have fixed the freaking symlink error.