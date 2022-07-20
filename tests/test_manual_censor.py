from test_commons import *
from contentCensoring import *

print("initiating test sequence...")
mdata = censorInterface(
    "test_title",
    None,
    "test_content",
)
print("interface closed.")
print("collected data:", mdata)
