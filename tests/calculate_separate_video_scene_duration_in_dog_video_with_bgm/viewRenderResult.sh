ls -1 output | awk '{print "ffplay -i output/"$1" -autoexit" }' > viewer.sh
bash viewer.sh