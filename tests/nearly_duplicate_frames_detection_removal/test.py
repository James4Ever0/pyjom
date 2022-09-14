source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.gif"  # this is evil. it defeats my shit.

# is it still image?
# we can also detect more shits. right?
import scenedetect

stats_file_path = "output.csv"
cuts = scenedetect.detect(
    video_path=source, stats_file_path=stats_file_path, show_progress=True
)

import pandas

df = pandas.read_csv(stats_file_path)
