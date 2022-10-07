killall -s KILL motion
# ffmpeg -re -i ../../samples/video/LlfeL29BP.mp4 -f v4l2 /dev/video0 &
motion -c mconfig.conf

# to conclude, this is only useful for webcams, not for media file processing.
# are you sure if you want to capture shits over webcams by this?