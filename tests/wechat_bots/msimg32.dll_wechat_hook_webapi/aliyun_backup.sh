current_dir_name=$(pwd | awk -F "/" '{print $NF}')

find -depth -maxdepth 1 -type d | grep ./ | xargs -iabc aliyunpan backup --ow abc /$current_dir_name/
aliyunpan backup --ow ./ /