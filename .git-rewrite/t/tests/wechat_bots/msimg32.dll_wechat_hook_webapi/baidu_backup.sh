current_dir_name=$(pwd | awk -F "/" '{print $NF}')

BaiduPCS-Go upload --norapid  --policy rsync * /$current_dir_name/