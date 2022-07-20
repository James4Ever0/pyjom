import time
from playwright.sync_api import Playwright, sync_playwright

import http.server
import socketserver
import multiprocessing
import os

PORT = 8022
import shutil
import os
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    proc = multiprocessing.Process(target=httpd.serve_forever,daemon=True)
    proc.start()
    # thread.run()


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # browser = playwright.chromium.launch(headless=False,args=["--allow-file-access-from-files","--disable-web-security",'--js-flags="--expose-gc"'])
    context = browser.new_context(accept_downloads=True)
    # Open new page
    page = context.new_page()
    # the effect is ugly.
    # it is meant to be used as a webpage.
    # Go to file:///media/root/help/pyjom/tests/mmd_human_dance_pose/test_mmd_three_js_record/mmd_record/miku_dance_recorder/webgl_loader_mmd.html
    while True:
        try:
            page.goto("http://localhost:{}/index.html".format(PORT))
            # page.goto("http://localhost:{}/webgl_loader_mmd.html  ".format(PORT))
            break
        except:
            time.sleep(1)
    # context.close()
    seconds = 0 # infinite patience.
    # it has things.
    with page.expect_download(timeout=1000*seconds) as download_info:
        print("downloading things:")
        download = download_info.value
        path = download.path() # this is a promise.
        # print(dir(download_info))
        # print(dir(download))
        # print(dir(path)) #  this is a os.path object.
        filepath = "ideal.webm"
        if os.path.exists(filepath):
            os.remove(filepath)
        shutil.copy(path,filepath)
        # print("value:",download_info,download,path)
        # file will gone if not saved.
        # breakpoint()
        print("DOWNLOAD COMPLETE")
    # print("PAGE OPENED")
    # time.sleep(1000000)
    context.close()
    browser.close()
    exit() # will it reach here?
    os.abort()
with sync_playwright() as playwright:
    run(playwright)
