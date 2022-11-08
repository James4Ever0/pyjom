from recover import recover
from rewrite import rewrite

def recover_and_rewrite(source_old):
    intermediate = recover(source_old)
    source_new = rewrite(intermediate)
    return source_new

if __name__ == '__main__':
    comby = Comby()

    source_old = open('new_test.py','r').read()
    source_new = recover_and_rewrite(source_old)
    print(source_new)