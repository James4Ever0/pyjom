# sudo apt-get install build-essential git cmake pkg-config libboost-all-dev  qtbase5-dev libqt5svg5-dev qtscript5-dev qttools5-dev qttools5-dev-tools libqt5opengl5-dev qtmultimedia5-dev libqt5multimedia5-plugins libqt5serialport5-dev libsuperlu-dev  liblz4-dev libusb-1.0-0-dev liblzo2-dev libpng-dev libjpeg-dev libglew-dev freeglut3-dev libfreetype6-dev libjson-c-dev qtwayland5 libmypaint-dev libopencv-dev libturbojpeg-dev

# sudo apt-get install libmypaint-dev

# git clone --depth 1 https://github.com/opentoonz/opentoonz

mkdir -p $HOME/.config/OpenToonz
cp -r opentoonz/stuff $HOME/.config/OpenToonz/

cd opentoonz/thirdparty/tiff-4.0.3
./configure --with-pic --disable-jbig
make -j$(nproc)
cd ../../

cd toonz
mkdir build
cd build
cmake ../sources
make -j$(nproc)

sudo make install

ln -s /opt/opentoonz/bin/opentoonz /usr/bin/opentoonz