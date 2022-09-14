import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f",'--ffmpeg-filters', help="show ffmpeg filters")
parser.add_argument('-r','--random', help='randomize output')
flags = parser.parse_args()

if flags.f:
    if 