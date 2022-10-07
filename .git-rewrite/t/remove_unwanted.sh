# git filter-branch --force --index-filter \
#   'git rm -rf --cached --ignore-unmatch samples' \
#   --prune-empty --tag-name-filter cat -- --all

git filter-branch --force --index-filter \
  'git rm -rf --cached --ignore-unmatch tests/video_detector_tests/videoflow' \
  --prune-empty --tag-name-filter cat -- --all