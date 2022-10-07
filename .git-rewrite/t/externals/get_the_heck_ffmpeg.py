mystr = "-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --enable-pocketsphinx --enable-librsvg --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-chromaprint --enable-frei0r --enable-libx264 "

mystr = mystr.split(" ")

mylibs = []
for elem in mystr:
    a = elem.replace("-","").replace(" ","").replace("enable","")
    if len(a) <=2:
        continue
    if a.startswith("lib"):
        a +="-dev"
        mylibs.append(a)
    else:
        a+= "-dev"
        b = "lib"+a
        mylibs.append(a)
        mylibs.append(b)

for lib in mylibs:
    print("yes | apt install {}".format(lib))