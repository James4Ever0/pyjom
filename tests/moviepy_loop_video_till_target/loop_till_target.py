import os

# moviepy's shit.
from moviepy.editor import VideoFileClip  # , concatenate_videoclips

# import moviepy.video.fx.all as vfx


def main(
    f_in: str,
    target_secs: float,
    f_out: str = "",
    in_place: bool = True,
    debug: bool = False,
    # accuracy_float:int=4
    # audio:bool=False, # it will cause trouble?
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

    clip = VideoFileClip(f_in)
    # if not audio:
    #     clip = clip.without_audio()
    # newclip = clip.fx(vfx.time_mirror) # error?
    # newclip = clip
    import ffmpeg

    file_input_split = ffmpeg.input(f_in).filter_multi_output(
        "split"
    )  # this is infinite split.

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
    file_input_original = file_input_split[0].filter_multi_output("split")
    file_input_reverse = (
        file_input_split[1].filter("reverse").filter_multi_output("split")
    )

    for index, signal in enumerate(loopStrategy):
        mindex = index // 2
        if signal == 1:
            file_input = file_input_original[mindex]
            clips.append(file_input)
        else:
            file_input_reverse2 = file_input_reverse[mindex]
            clips.append(file_input_reverse2)

    # final = concatenate_videoclips(clips)
    final = ffmpeg.concat(*clips)
    finalVideoDuration = len(loopStrategy) * videoDuration

    with tempfile.NamedTemporaryFile(
        "w+",
        suffix=f".{fileExtension}",
    ) as f:
        tmpFilePath = f.name
        # warning! what is the audio shit?
        # print("TMP FILE PATH?",tmpFilePath)
        # breakpoint()
        # final.write_videofile(tmpFilePath, fps=clip.fps)
        # finalVideoDuration = final.duration
        final.output(tmpFilePath).run(overwrite_output=True)
        shutil.copy(tmpFilePath, targetFilePath)
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

    # parser.add_argument(
    #     "-a",
    #     "--audio",
    #     help="include audio from input",
    #     action="store_true",
    #     default=False,
    # )
    parser.add_argument(
        "-t", "--target", help="target seconds", required=True, type=float
    )

    args = parser.parse_args()
    if not args.replace:
        assert args.output != ""
    main(
        args.input,
        args.target,
        f_out=args.output,
        in_place=args.replace,
        # audio=args.audio
    )
