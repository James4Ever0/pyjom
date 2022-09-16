VIDEO="/root/Desktop/works/pyjom/samples/video/cute_cat_gif.mp4"

# ./mpegflow $VIDEO > output.txt

mkdir -p examples/vis_dump && ./mpegflow $VIDEO | ./vis $VIDEO examples/vis_dump