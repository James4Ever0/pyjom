cd FAST-VQA
VIDEO="/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.mp4"
python3 vqa.py -o ./options/fast/f3dvqa-b.yml -v $VIDEO -d cpu
# The quality score of the video is 0.11833.