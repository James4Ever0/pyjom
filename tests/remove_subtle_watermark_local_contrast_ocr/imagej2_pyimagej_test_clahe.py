# source:
# https://github.com/seung-lab/Alembic/blob/575c8ed2a5f8789e65de652c9349993c530de718/src/archive/import/convert_dir_to_CLAHE.py
# https://github.com/search?q=mpicbg.ij.clahe&type=code

# for jpython you need to append all jar absolute paths to sys.path. grammar shall be identical.

import jpype
import jpype.imports
from jpype.types import *

# jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/jars/*")
# jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/jars/*/*")
# jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins/*")
# jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins/*/*")

jpype.startJVM(
    classpath=[
        "/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/jars/*",
        "/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins/*",
    ]
)


from ij import IJ
import os

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
output_fn = "imagej_output.jpg"
imp = IJ.openImage(fn)

Flat.getFastInstance().run(
    imp, blocksize, histogram_bins, maximum_slope, mask, composite
)
IJ.save(imp, output_fn)

Flat.getFastInstance().run(
    imp, blocksize, histogram_bins, maximum_slope, mask, composite
)
# ImageConverter(imp).convertToGray8()

IJ.save(imp, "imagej_double.jpg")

# # Create an ImageJ2 gateway with the newest available version of ImageJ2.
# # fiji_path = "/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app"
# # ij = imagej.init(fiji_path)
# import scyjava
# # plugins_dir = '/Applications/Fiji.app/plugins'
# # plugins_dir = "/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins"
# # scyjava.config.add_option(f'-Dplugins.dir={plugins_dir}')
# # scyjava.config.add_repositories({'scijava.public': 'https://maven.scijava.org/content/groups/public'})
# import imagej

# ij = imagej.init()

# # Load an image.
# image_url = "IWWS.jpeg"
# jimage = ij.io().open(image_url)

# # Convert the image from ImageJ2 to xarray, a package that adds
# # labeled datasets to numpy (http://xarray.pydata.org/en/stable/).
# image = ij.py.from_java(jimage)

# # Display the image (backed by matplotlib).
# # ij.py.show(image, cmap='gray')
# # print('IMAGE',image)
# # d = dir(ij)
# # print(d)
# # ['IJ', 'ResultsTable', 'RoiManager', 'WindowManager', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_access_legacy_class', '_check_legacy_active', 'animation', 'app', 'appEvent', 'command', 'compareTo', 'console', 'context', 'convert', 'dataset', 'display', 'dispose', 'equals', 'event', 'eventHistory', 'get', 'getApp', 'getClass', 'getContext', 'getIdentifier', 'getInfo', 'getLocation', 'getPriority', 'getShortName', 'getTitle', 'getVersion', 'hashCode', 'icon', 'imageDisplay', 'input', 'io', 'launch', 'legacy', 'log', 'lut', 'main', 'menu', 'module', 'notebook', 'notify', 'notifyAll', 'object', 'op', 'options', 'overlay', 'platform', 'plugin', 'prefs', 'py', 'recentFile', 'rendering', 'sampler', 'scifio', 'screenCapture', 'script', 'setContext', 'setInfo', 'setPriority', 'startup', 'status', 'text', 'thread', 'toString', 'tool', 'ui', 'update', 'uploader', 'wait', 'widget', 'window']
# # p = ij.plugin
# # print(dir(p))
# clahe = scyjava.jimport('mpicbg')
