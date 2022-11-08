from recover import recover
from rewrite import rewrite

def recover_and_rewrite(source_old):
    intermediate = recover(source_old)
    return rewrite(intermediate)

if __name__ == '__main__':