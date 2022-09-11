mkdir pip_examine
cat pip_motion_cropdetect.log | awk -F 't:' '{print $2}' | awk '{print "ffmpeg -ss " $1 " -i /root/Desktop/works/pyjom/samples/video/LiEIfnsvn.mp4 -vframes 1 pip_examine/screenshot_" i++ ".jpg" }' > pip_examine.sh
bash pip_examine.sh
