import os
from moviepy.video import VideoClip


def main(
    f_in: str,
    target_secs: float,
    f_out: str = "",
    in_place: bool = True,
    debug: bool = False,
    # accuracy_float:int=4
):
    assert os.path.exists(f_in)
    assert target_secs > 0
    # target_secs_str =("{"+f':.{accuracy_float}f'+"}").format(target_secs)
    if not in_place:
        assert f_out != ""
    videoDuration = ...
    import math

    fileExtension = f_in.split(".")[-1]
    assert fileExtension != ""

    loopStrategy = [
        (-1) ** i for i in range(math.ceil(target_secs / videoDuration))
    ]  # zero division error?
    if debug:
        print("Loop strategy:")
        print(loopStrategy)
    for signal in loopStrategy:
        ...
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
        "-t", "--target", help="target seconds", required=True, type=float
    )

    args = parser.parse_args()
    if not args.replace:
        assert args.output != ""
    main(args.input, args.target, f_out=args.output, in_place=args.replace)
