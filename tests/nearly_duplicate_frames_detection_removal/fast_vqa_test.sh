cd FAST-VQA
# VIDEO="/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.mp4"
# The quality score of the video is 0.11833.
VIDEO="/root/Desktop/works/pyjom/samples/video/kitty_flash_15fps.mp4"
# The quality score of the video is 0.12778.

# nothing serious. it does not produce significant shits.
python3 vqa.py -o ./options/fast/f3dvqa-b.yml -v $VIDEO -d cpu

# another feature is that this video produces a large area in white, which is not what we really want.

# use knn?
# k=5