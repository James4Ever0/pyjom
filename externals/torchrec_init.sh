# git clone --depth 1 --recurse-submodules https://github.com/pytorch/torchrec
cd torchrec
# modify the freaking setup.py first. don't want no trouble.
# python3 setup.py install
export CUB_DIR=/usr/include/cub
export CUDA_BIN_PATH=/usr/lib/nvidia-cuda-toolkit
export CUDACXX=/usr/bin/nvcc
cp -R /usr/local/lib/python3.9/dist-packages/torch/include/* third_party/fbgemm/fbgemm_gpu/include # great shit.
python3 setup.py install 

# the freaking fix.
# cd third_party/fbgemm/fbgemm_gpu
# cp -R /usr/local/lib/python3.9/dist-packages/torch/include/* ./include # great shit.
# export CUB_DIR=/usr/include/cub
# export CUDA_BIN_PATH=/usr/lib/nvidia-cuda-toolkit
# export CUDACXX=/usr/bin/nvcc
# python3 setup.py install 

