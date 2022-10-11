git clone --depth 1 https://git.ffmpeg.org/ffmpeg.git ffmpeg/
git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
cd nv-codec-headers && sudo make install && cd ..
yes | apt-get install build-essential yasm cmake libtool libc6 libc6-dev unzip wget libnuma1 libnuma-dev libchromaprint-dev frei0r-plugins-dev libaom-dev libiec61883-dev libass-dev libbluray-dev libbs2b-dev libcodec2-dev libgsm1-dev libopenjp2-7-dev librsvg2-dev libzmq3-dev libomxil-bellagio-dev libcdio-paranoia-dev libsrt-gnutls-dev libopenh264-dev

# yes | apt-get   build-dep ffmpeg # has unmet dependencies.
# git clone https://github.com/Haivision/srt.git libsrt
# cd libsrt/
# git checkout -b work v1.4.1
# sudo apt-get install tclsh pkg-config cmake libssl-dev build-essential
# ./configure 
# make
# sudo make install
# sudo ldconfig
# cd ..
# yes | apt install ladspa-dev
# yes | apt install libaom-dev
# yes | apt install libass-dev
# yes | apt install libbluray-dev
# yes | apt install libbs2b-dev
# yes | apt install libcaca-dev
# yes | apt install libcdio-dev
# yes | apt install libcodec2-dev
# yes | apt install libdav1d-dev
# yes | apt install libflite-dev
# yes | apt install libfontconfig-dev
# yes | apt install libfreetype-dev
# yes | apt install libfribidi-dev
# yes | apt install libgme-dev
# yes | apt install libgsm-dev
# yes | apt install libjack-dev
# yes | apt install libmp3lame-dev
# yes | apt install libmysofa-dev
# yes | apt install libopenjpeg-dev
# yes | apt install libopenmpt-dev
# yes | apt install libopus-dev
# yes | apt install libpulse-dev
# yes | apt install librabbitmq-dev
# yes | apt install librubberband-dev
# yes | apt install libshine-dev
# yes | apt install libsnappy-dev
# yes | apt install libsoxr-dev
# yes | apt install libspeex-dev
# yes | apt install libsrt-dev
# yes | apt install libssh-dev
# yes | apt install libtheora-dev
# yes | apt install libtwolame-dev
# yes | apt install libvidstab-dev
# yes | apt install libvorbis-dev
# yes | apt install libvpx-dev
# yes | apt install libwebp-dev
# yes | apt install libx265-dev
# yes | apt install libxml2-dev
# yes | apt install libxvid-dev
# yes | apt install libzimg-dev
# yes | apt install libzmq-dev
# yes | apt install libzvbi-dev
# yes | apt install lv2-dev
# yes | apt install liblv2-dev
# yes | apt install omx-dev
# yes | apt install libomx-dev
# yes | apt install openal-dev
# yes | apt install libopenal-dev
# yes | apt install opencl-dev
# yes | apt install libopencl-dev
# yes | apt install opengl-dev
# yes | apt install libopengl-dev
# yes | apt install sdl2-dev
# yes | apt install libsdl2-dev
# yes | apt install pocketsphinx-dev
# yes | apt install libpocketsphinx-dev
# yes | apt install librsvg-dev
# yes | apt install libmfx-dev
# yes | apt install libdc1394-dev
# yes | apt install libdrm-dev
# yes | apt install chromaprint-dev
# yes | apt install libchromaprint-dev
# yes | apt install frei0r-dev
# yes | apt install libfrei0r-dev
# yes | apt install libx264-dev
cd ffmpeg
# libchromaprint: audio fingerprint
# frei0r: video effects
# libaom-dev: av1 video codec
# ./configure --enable-nonfree --enable-cuda-nvcc --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64 --disable-static --enable-shared
# ./configure --enable-gpl --enable-nonfree --enable-pthreads --extra-libs=-lstdc++ --enable-cuda-nvcc --enable-cuvid --enable-nvenc --enable-shared --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --enable-libnpp --extra-ldflags=-L/usr/local/cuda/lib64 --disable-static 

# add libspeex
# why libspeex is not working?
# you'd better build this shit from source.
# because libspeex1 rebuild or something.
###LAST WORKING ONE
./configure --toolchain=hardened  --arch=amd64 --enable-gpl --enable-nonfree --enable-pthreads --extra-libs=-lstdc++ --enable-cuda-nvcc --enable-cuvid --enable-nvenc --enable-shared --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --enable-libnpp --extra-ldflags=-L/usr/local/cuda/lib64 --disable-static --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libsrt --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --disable-sndio --enable-pocketsphinx --enable-librsvg --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared --enable-libopenh264 # wtf?
### LAST WORKING ONE

# ./configure --enable-gpl --enable-nonfree --enable-pthreads --extra-libs=-lstdc++ --enable-cuda-nvcc --enable-cuvid --enable-nvenc --enable-shared --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --enable-libnpp --extra-ldflags=-L/usr/local/cuda/lib64 --disable-static --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --disable-sndio --enable-pocketsphinx --enable-librsvg --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared

# ./configure --prefix=/usr/local/ffmpeg --enable-gpl --enable-nonfree --enable-pthreads --extra-cflags=-g --extra-cflags=-O0 --extra-libs=-lstdc++ --extra-cxxflags=-g --extra-cxxflags=-O0 --extra-cxxflags=-fpermissive --enable-debug=3 --disable-optimizations --disable-stripping --disable-x86asm --enable-cuda-nvcc --enable-cuvid --enable-shared --enable-nvenc --enable-shared --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64
make -j8
make install
# this is not distributable. non-free nvenc

# without mp3!
# original compiling flags:
# --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --disable-sndio --enable-pocketsphinx --enable-librsvg --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared