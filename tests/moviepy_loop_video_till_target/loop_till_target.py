import os
import moviepy

def main(f_in:str, target_secs:float,f_out:str="", in_place:bool=True, accuracy_float:int=4):
    assert os.path.exists(f_in)
    assert target_secs >0
    target_secs_str =("{"+f':.{accuracy_float}f'+"}").format(target_secs)
    if not in_place:
        assert f_out != ""

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input file", required=True)
    parser.add_argument("-o", "--output", dest="output file", default="")