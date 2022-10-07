mkdir opencv
cd opencv

wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.x.zip
unzip opencv.zip
unzip opencv_contrib.zip
# Create build directory and switch into it
mkdir -p build && cd build
# Configure
cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules -DWITH_CUDA=ON ../opencv-4.x
# Build
cmake --build .
make install

bash /media/root/help/pyjom/externals/opencv_py_reset.sh
