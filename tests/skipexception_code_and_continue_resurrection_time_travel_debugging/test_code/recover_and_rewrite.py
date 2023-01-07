from recover import recover
from rewrite import rewrite

def recover_and_rewrite(source_old,no_rewrite=False):
    intermediate = recover(source_old)
    if not no_rewrite:
        source_new = rewrite(intermediate)
    else: source_new=intermediate
    return source_new

if __name__ == '__main__':
    # from comby import Comby
    # comby = Comby()
    source_old = open('new_test.py','r').read()
    source_new = recover_and_rewrite(source_old)
    print(source_new)