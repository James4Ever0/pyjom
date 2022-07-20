export http_proxy=""
export https_proxy=""

env http_proxy="" https_proxy="" python3 setup.py build
env http_proxy="" https_proxy=""  python3 setup.py install