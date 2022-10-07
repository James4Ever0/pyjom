bash ~/mount_disks.sh
# mkdir /media/root/help/AGI/pyjom
# mkdir /media/root/Toshiba30003/pyjom # select the last one.
# mkdir /media/root/Jumpcut/pyjom

# rclone sync -P . /media/root/help/AGI/pyjom

# this one is different!

# rclone sync -P . /media/root/Toshiba30003/pyjom
# rclone sync -P . /media/root/Jumpcut/pyjom # really freaking slow.
# cd /media/root/help/pyjom # base dir
cd $(mount | grep -E "/media/root/help" | awk '{print $3}')
mount | grep -E "/media/root/Toshiba3000|/media/root/Jumpcut|/media/root/Seagate1000" | awk '{print $3}' | xargs -iabc mkdir abc/pyjom
cd pyjom # important. my shit fucked...
# pwd
# exit
# mount | grep -E "/media/root/help|/media/root/Toshiba3000|/media/root/Jumpcut|/media/root/Seagate1000" | awk '{print $3}' | xargs -iabc mkdir abc/pyjom
# mount | grep -E "/dev/sde1|/dev/sdd1|/dev/sda2" | awk '{print $3}' | xargs -iabc rclone sync -P . abc/pyjom
mount | grep -E "/media/root/Toshiba3000|/media/root/Jumpcut|/media/root/Seagate1000"| awk '{print $3}' | xargs -iabc rclone sync -P . abc/pyjom

# remote sync
bash remote_backup.sh