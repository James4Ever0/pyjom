ls -1 output | awk '{print "ffplay -i output/"$1" -autoexit; sleep 3" }' > viewer.sh
bash viewer.sh