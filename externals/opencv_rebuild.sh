cd opencv
# cd build
# rm -rf build
# mkdir build
cd build
# Configure
# do not use anaconda
conda deactivate
# override anaconda in $PATH
# export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games:/usr/local/cuda-10.2/bin:/snap/bin
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games:/snap/bin # ignore incompatible nvcc
# to download things.
# export HTTP_PROXY=http://192.168.43.78:8899
# export http_proxy=http://192.168.43.78:8899
# export https_proxy=http://192.168.43.78:8899
# export HTTPS_PROXY=http://192.168.43.78:8899
# export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH
# need turn cuda on.
# switch to gcc-9, lower than 10
cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-4.x/modules -DHTTP_PROXY=http://192.168.43.78:38457 -DWITH_CUDA=ON ../opencv-4.x
# Build
cmake --build .
make install 
# cd /media/root/help/pyjom/externals/
# bash /media/root/help/pyjom/externals/opencv_py_reset.sh

# --   OpenCV modules:
# --     To be built:                 alphamat aruco barcode bgsegm bioinspired calib3d ccalib core cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev datasets dnn dnn_objdetect dnn_superres dpm face features2d flann freetype fuzzy gapi hdf hfs highgui img_hash imgcodecs imgproc intensity_transform java line_descriptor mcc ml objdetect optflow phase_unwrapping photo plot python2 python3 quality rapid reg rgbd saliency sfm shape stereo stitching structured_light superres surface_matching text tracking ts video videoio videostab wechat_qrcode xfeatures2d ximgproc xobjdetect xphoto
# --     Disabled:                    world
# --     Disabled by dependency:      -
# --     Unavailable:                 cvv julia matlab ovis viz
# --     Applications:                tests perf_tests apps