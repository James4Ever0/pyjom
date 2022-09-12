ls -1 output | awk '{print "ffplay -i "$1" -autoexit" }' > viewer.sh
bash viewer.sh