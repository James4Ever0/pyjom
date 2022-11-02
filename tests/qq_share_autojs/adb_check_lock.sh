function checkScreen {
  adb -s 192.168.10.3:5555 shell dumpsys window | grep mDreamingLockscreen=false
  if [[ $? -eq 1 ]]; then
    echo "phone locked"
    bash adb_unlock.sh
    sleep 2
  else
    echo "phone unlocked"
    exit
  fi
}

while true
do
  checkScreen
done
