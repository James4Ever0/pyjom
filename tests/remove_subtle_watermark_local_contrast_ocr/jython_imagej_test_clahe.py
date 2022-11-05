import os
import sys

cpdirs = [
    "/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/jars/",
    "/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins/",
]

for d in cpdirs:
    abspath = os.path.abspath(d)
    files = os.listdir(abspath)
    jars = [f for f in files if f.endswith(".jar")]
    for f in jars:
        abs_jarpath = os.path.join(abspath, f)
        sys.path.append(abs_jarpath)

# now begin work.

from ij import IJ

# import os

from mpicbg.ij.clahe import Flat
from ij.process import ImageConverter

# http://fiji.sc/wiki/index.php/Enhance_Local_Contrast_(CLAHE)
# http://fiji.sc/cgi-bin/gitweb.cgi?p=mpicbg.git;a=blob;f=mpicbg/ij/clahe/PlugIn.java;h=663153764493547de560c08ee11f2e6b1e7e1a32;hb=HEAD

# dir = "/usr/people/tmacrina/seungmount/research/Julimaps/datasets/AIBS_pilot_v1/0_raw/"

blocksize = 40
histogram_bins = 255
maximum_slope = 5
mask = "*None*"
composite = False
mask = None

# files = os.listdir(dir)
# files.sort()
# for file in files:
#      if file.endswith(".tif")
# fn = os.path.join(dir, 'original.tif')
fn = "IWWS.jpeg"
imp = IJ.openImage(fn)
output_fn = "imagej_output_jython.jpg"
imp = IJ.openImage(fn)

Flat.getFastInstance().run(
    imp, blocksize, histogram_bins, maximum_slope, mask, composite
)
IJ.save(imp, output_fn)

Flat.getFastInstance().run(
    imp, blocksize, histogram_bins, maximum_slope, mask, composite
)
# ImageConverter(imp).convertToGray8()

IJ.save(imp, "imagej_double_jython.jpg")
