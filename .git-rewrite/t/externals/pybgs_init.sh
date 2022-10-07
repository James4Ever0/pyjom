# opencvdir=""
# env OpenCV_DIR= pip3 install pybgs
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games:/usr/local/cuda-10.2/bin:/snap/bin
cd bgslibrary
python3 setup.py build
python3 setup.py install