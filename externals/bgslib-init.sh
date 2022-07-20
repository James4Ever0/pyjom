git clone --recursive https://github.com/andrewssobral/bgslibrary.git

cd bgslibrary

cd build
cmake ..
make -j $(nproc)

####### OPTIONAL #######
make install
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib # this is to ensure the path.
export LD_LIBRARY_PATH
# for debug: echo $LD_LIBRARY_PATH
# Next, copy the <<config>> folder from bgslibrary repository to your working space.
# Now you can run bgslibrary by: bgs -i video.avi
########################

cd ..
chmod +x *.sh
./run_video.sh
./run_camera.sh
./run_demo.sh
./run_demo2.sh