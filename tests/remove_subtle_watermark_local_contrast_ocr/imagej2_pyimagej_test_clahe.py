import jpype

jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/jars/*")
jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/jars/*/*")
jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins/*")
jpype.addClassPath("/root/Desktop/works/pyjom/tests/remove_subtle_watermark_local_contrast_ocr/imagej_fiji_linux/Fiji.app/plugins/*/*")

jpype.startJVM()

from ij import ImageJ

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