git clone --depth 1 --recurse-submodules https://github.com/dmlc/dgl.git
cd dgl # set up my fucking fastgithub proxy!
# git submodule update --init --recursive
mkdir build
cd build
cmake -DUSE_CUDA=ON ..
make -j4
cd ..
pip3 install ./python # the way to install this shit.
# cd ../python
# python3 setup.py install