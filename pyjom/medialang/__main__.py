from pyjom.medialang.core import *

if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-f",
        "--file",
        help="medialang file path that needed to be formatted.",
        type=str,
        required=True,
    )
    parse_result = arg_parser.parse_args()
    file_path = parse_result.file
    mdl = Medialang(script_path=file_path)  # will be parsed.
    if mdl.script_obj is not None:
        mdl.prettify(inplace=True)
        print("prettified: ", mdl.script_path)
    # pass
