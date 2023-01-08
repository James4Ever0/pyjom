src = "/root/Desktop/works/pyjom/samples/video/kitty_flash.gif"

import pathlib, sys  # great.

site_path = pathlib.Path("/usr/local/lib/python3.9/site-packages")
cv2_libs_dir = (
    site_path / "cv2" / f"python-{sys.version_info.major}.{sys.version_info.minor}"
)
print(cv2_libs_dir)
cv2_libs = sorted(cv2_libs_dir.glob("*.so"))
if len(cv2_libs) == 1:
    print("INSERTING:", cv2_libs[0].parent)
    sys.path.insert(1, str(cv2_libs[0].parent))

from caer.video.frames_and_fps import get_fps_float

fps = get_fps_float(src)
print("FPS:", fps)  # 10? was very inaccurate for me
# now it is good. 9.5
