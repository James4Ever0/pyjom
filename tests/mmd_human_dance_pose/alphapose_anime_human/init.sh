git clone https://github.com/MVIG-SJTU/AlphaPose.git
# git pull origin pull/592/head if you use PyTorch>=1.5
cd AlphaPose


# 4. install
# export PATH=/usr/local/cuda/bin/:$PATH
# export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH
export PATH=/usr/lib/nvidia-cuda-toolkit/bin/:$PATH
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH
export http_proxy=""
export https_proxy=""
python3 -m pip install cython cython_bbox
sudo apt-get install libyaml-dev
################Only For Ubuntu 18.04#################
locale-gen C.UTF-8
# if locale-gen not found
sudo apt-get install locales
export LANG=C.UTF-8
######################################################
export MAX_JOBS=10
# python3 setup.py install
python3 setup.py build # already locally importable. do not install
# python3 setup.py install --root /usr/lib/python3/dist-packages/ # install to given location
# pip3n install mediapipe --no-dependencies
# python3 setup.py install --old-and-unmanagible # without building egg