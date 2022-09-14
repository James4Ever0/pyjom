import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f",'--ffmpeg-filters', help="show ffmpeg filters")
parser.add_argument('-r','--random', help='randomize output')
flags = parser.parse_args()
randomize=False

if flags.r:
    randomize=True

if flags.f:
    command = """ffmpeg -filters 2>/dev/null | grep "\\->" | awk '{print $2}' | shuf | xargs -I abc bash -c "ffmpeg -h filter=abc  2>/dev/null ; echo '________________________________________';echo " |  less"""
    os.system(command)