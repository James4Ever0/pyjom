import os
def main(f_in:str, target_secs:float,f_out:str="", in_place:bool=True, accuracy_float:int=4):
    assert os.path.exists(f_in)
    assert target_secs >0
    
    if not in_place:
        assert f_out != ""

if __name__ == '__main__':
    import argparse