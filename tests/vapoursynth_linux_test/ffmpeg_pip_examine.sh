mkdir pip_examine
cat pip_motion_cropdetect.log | awk -F 't:' '{print $2}' | awk '{print "ffmpeg -y -ss " $1 " -i /root/Desktop/works/pyjom/samples/video/LiEIfnsvn.mp4 -vf " $2 " -vframes 1 pip_examine/screenshot_" i++ ".jpg" }' > pip_examine.sh
bash pip_examine.sh
