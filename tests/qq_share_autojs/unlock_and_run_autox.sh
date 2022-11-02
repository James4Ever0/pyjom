bash adb_check_lock.sh 

function autox_run {
  adb -s 192.168.10.3:5555 shell touch /storage/emulated/0/flag
  bash adb_autox_launch.sh
  
  while true
  do
    adb -s 192.168.10.3:5555 shell cat /storage/emulated/0/flag
    if [[ $? -eq 1 ]]
    then
      echo "script complete"
      exit
    else
      echo "script running"
      sleep 1
    fi
  done
}
while true
do
  autox_run
  # you need to ensure the script run as expected.
done
