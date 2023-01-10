import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.time_mirror import time_mirror

def main(
    f_in: str,
    target_secs: float,
    f_out: str = "",
    in_place: bool = True,
    debug: bool = False,
    # accuracy_float:int=4
    audio:bool=False, # it will cause trouble?
):

    # print("___")
    # print("AUDIO?",audio)
    # print("IN PLACE?",in_place)
    # print("___")

    assert os.path.exists(f_in)
    assert target_secs > 0
    
    # target_secs_str =("{"+f':.{accuracy_float}f'+"}").format(target_secs)
    targetFilePath = f_out
    if not in_place:
        assert f_out != ""
    else:
        targetFilePath = f_in

    clip = VideoFileClip(f_in,audio=audio)
    if not audio:
        clip = clip.without_audio()
    # newclip = clip.fx(time_mirror) # error?
    # newclip =clip

    videoDuration = clip.duration
    import math
    import tempfile
    import shutil

    fileExtension = f_in.split(".")[-1]
    assert fileExtension != ""

    loopStrategy = [
        (-1) ** i for i in range(math.ceil(target_secs / videoDuration))
    ]  # zero division error?
    if debug:
        print("Loop strategy:")
        print(loopStrategy)
    clips = []
    for signal in loopStrategy:
        if signal == 1:
            clips.append(clip)
        else:
            clips.append(newclip)

    final = concatenate_videoclips(clips)

    with tempfile.NamedTemporaryFile('w+',suffix=f".{fileExtension}",) as f:
        tmpFilePath = f.name
        # warning! what is the audio shit?
        print("TMP FILE PATH?",tmpFilePath)
        breakpoint()
        final.write_videofile(tmpFilePath, fps=clip.fps)
        finalVideoDuration = final.duration
        shutil.copy(tmpFilePath,targetFilePath)
    return finalVideoDuration


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file", required=True, type=str)
    parser.add_argument("-o", "--output", help="output file", default="", type=str)
    parser.add_argument(
        "-r",
        "--replace",
        help="replace original input file",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-a",
        "--audio",
        help="include audio from input",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-t", "--target", help="target seconds", required=True, type=float
    )

    args = parser.parse_args()
    if not args.replace:
        assert args.output != ""
    main(args.input, args.target, f_out=args.output, in_place=args.replace,audio=args.audio)
