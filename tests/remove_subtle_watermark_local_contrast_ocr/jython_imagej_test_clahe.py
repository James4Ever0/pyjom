import os
import sys

cpdirs = ["/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/jars/","/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins/"]

for d in cpdirs:
    abspath = os.path.abspath(d)
    files = os.listdir(abspath)
    jars = [f for f in files if f.endswith(".jar")]
    for f in jars:
        abs_jarpath = os.path.join(abspath, f)
        sys.path.append(abs_jarpath)

# now begin work.