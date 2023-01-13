# 0 * * * * /usr/bin/python3 /root/Desktop/works/pyjom/tests/download_sections_video_portion_partial_download_youtube_yt_dlp_bilibili/cron_update_cookies_stored_under_root_home.py

import os
import shutil

cookies_path = "/root/.browser_cookies_exported"

if not (os.path.exists(cookies_path) or os.path.isdir(cookies_path)):
    if os.path.isfile(cookies_path):
        os.remove(cookies_path)
    elif os.path.isdir(cookies_path):
        shutil.rmtree(cookies_path)
    elif os.path.islink(cookies_path):
        os.unlink(cookies_path)
    os.mkdir(cookies_path)

import yt_dlp

browser_names = ["firefox","chromium"]

for browser_name in browser_names:
    cookies = yt_dlp.cookies.extract_cookies_from_browser(browser_name)
    filepath = os.path.join(cookies_path,f"{browser_name}.cookies")
    cookies.save(filepath)