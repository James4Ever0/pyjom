from playwright.sync_api import Playwright, sync_playwright
import os
import shutil
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    # Open new page
    page = context.new_page()
    # page.goto("https://www.baidu.com")
    page.goto("file:///media/root/help/pyjom/tests/mmd_human_dance_pose/test_mmd_three_js_record/electron_record/electron-threejs-example/index3.html")
    # page.on("download", lambda download: print("downloaded to:",download.path()))
    seconds = 0 # infinite patience.
    # it has things.
    with page.expect_download(timeout=1000*seconds) as download_info:
        print("downloading things:")
        download = download_info.value
        path = download.path() # this is a promise.
        # print(dir(download_info))
        # print(dir(download))
        # print(dir(path)) #  this is a os.path object.
        shutil.copy(path,"ideal.webm")
        # print("value:",download_info,download,path)
        # file will gone if not saved.
        # breakpoint()
        print("DOWNLOAD COMPLETE")
    # # # ---------------------
    context.close()
    browser.close()
# import time
if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
        # time.sleep(1000000) # why you abort?
# this fucker just never waits.