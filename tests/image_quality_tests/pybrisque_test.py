from brisque import BRISQUE

# integrated svmutil.py and svm.py from that git repo.
# really strange.

brisq = BRISQUE()

# brisq.get_feature('/path')
image_path = "/root/Desktop/works/pyjom/tests/image_quality_tests/sample.bmp"
score = brisq.get_score(image_path)
print("score:",score)
# this is damn fast.