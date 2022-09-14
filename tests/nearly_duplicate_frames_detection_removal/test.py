# source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection.gif"  # this is evil. it defeats my shit.
source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps_blend.mp4"  # this is evil. it defeats my shit.
# source = "/root/Desktop/works/pyjom/samples/video/nearly_duplicate_frames_detection_30fps.gif"  # this is evil. it defeats my shit.

# is it still image?
# we can also detect more shits. right?

import sys
import os

os.chdir("../../")
sys.path.append(".")
from pyjom.commons import extract_span

import scenedetect

from caer.video.frames_and_fps import get_duration

stats_file_path = "/media/root/parrot/pyjom/tests/nearly_duplicate_frames_detection_removal/output.csv"
duration = get_duration(source)
print("DURATION:", duration)
cuts = scenedetect.detect(
    video_path=source, stats_file_path=stats_file_path, show_progress=True, 
    # detector=scenedetect.ContentDetector()
    detector=scenedetect.AdaptiveDetector(),
) # no fucking cuts???

import pandas

df = pandas.read_csv(stats_file_path)
print(df.head())
breakpoint()