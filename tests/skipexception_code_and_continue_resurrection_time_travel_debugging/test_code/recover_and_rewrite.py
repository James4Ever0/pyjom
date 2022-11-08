from recover import recover
from rewrite import rewrite

def recover_and_rewrite(source_old):
    intermediate = recover(source_old)
    source_new = rewrite(intermediate)
    return source_new

if __name__ == '__main__':
    source_old = open('')