import pathlib
import os
import requests
# again 0.0.0.0 not avaliable. must be localhost.
baseurl = "http://localhost:5700/"

# go-cqhttp client does not support adding friends, searching groups or something! test if we can login opqbot and this shit at the same time!

# it is working but unable to know if it is going to kill me.
import time
def check_connection():
    while True:
        try:
            response = requests.get(baseurl+"get_status", timeout=5)
            response_json = response.json()
            print("GO_CQHTTP STATUS:", response_json)
            data_json = response_json["data"]
            assert data_json["online"] == True
            print("connection ok")
            break
        except:
            import traceback
            traceback.print_exc()
            print("Connection error.")
            time.sleep(3)

def get_url(api):
    assert not api.startswith("/")
    return baseurl+api


def ensure_dir(download_path):
    if not os.path.exists(download_path):
        os.mkdir(download_path)

# api = "get_group_file_system_info"


def get_group_file(group_id, file_id, busid):
    api = "get_group_file_url"
    url = get_url(api)
    params = {"group_id": group_id, "file_id": file_id, "busid": busid}
    r = requests.get(url, params=params)
    # print(r.content)
    content = r.json()
    data = content["data"]
    if data!=None:
        download_url = data["url"]
        print("DOWNLOAD URL:", download_url)
        return download_url


def try_pass(function):
    try:
        function()
    except:
        pass


def downloader(url, filepath, skip_exist=True):
    lock = filepath+".lock"
    # check lock related operations.
    if os.path.exists(lock):
        try_pass(lambda: os.remove(lock))
        try_pass(lambda: os.remove(filepath))

    # do skip if flag "skip_exists" is set.
    if skip_exist:
        if os.path.exists(filepath):
            return  # no overwritting existing files.

    # download command
    cmd = 'curl -L -o "{}" "{}"'.format(filepath, url)

    # download main logic

    # touch lock first.
    pathlib.Path(lock).touch()

    os.system(cmd)
    try_pass(lambda: os.remove(lock))


def recursive_get_qq_group_files(api, group_id, basepath=None, folder_id=None, download_path="qq_group_file_download"):
    ensure_dir(download_path)
    if basepath is None:
        basepath = os.path.join(download_path, str(group_id))
    ensure_dir(basepath)
    if api == "get_group_root_files":
        params = {"group_id": group_id}  # integer for group id
    elif api == "get_group_files_by_folder":
        # integer for group id
        params = {"group_id": group_id, "folder_id": folder_id}
    else:
        raise Exception("Unknown recursive_get_qq_group_files api", api)

    url = get_url(api)
    r = requests.get(url, params=params)
# r = requests.get(url)

    content = r.json()

    # print(content)
    # breakpoint()
    data = content["data"]
    base_files = data["files"]
    base_folders = data["folders"]  # may walk recursively.
    base_files = [] if base_files == None else base_files
    base_folders = [] if base_folders == None else base_folders

    # print(base_files)
    for bfile in base_files:
        file_id = bfile["file_id"]  # prefixed with /, no need to check?
        # any expired files present? may cause download errors?
        file_name = bfile["file_name"]
        busid = bfile["busid"]
        download_url = get_group_file(group_id, file_id, busid)
        if download_url == None: continue
        filepath = os.path.join(basepath, file_name)
        print("FILEPATH:", filepath)
        yield download_url, filepath
        # download those base files!

    for bfolder in base_folders:
        # we have group_id though.
        folder_id = bfolder["folder_id"]
        folder_name = bfolder["folder_name"]
        new_basepath = os.path.join(basepath, folder_name)
        for download_url, filepath in recursive_get_qq_group_files("get_group_files_by_folder", group_id, basepath=new_basepath, folder_id=folder_id):
            yield download_url, filepath
        # all the same logic.
        # now do recursive folder search.

    # how to download these shits? curl?


def group_file_wholesale_downloader(group_id, download_path="qq_group_file_download", skip_exist=True):
    for download_url, filepath in recursive_get_qq_group_files("get_group_root_files", group_id, download_path=download_path):
        downloader(download_url, filepath, skip_exist=skip_exist)


# group_id = 927825838 # more files but no base_files.
# group_id = 537384511 # less files but have base_files

# make it dynamic!
download_path = "/root/Desktop/works/pyjom/tests/wechat_bots/msimg32.dll_wechat_hook_webapi/official_qq_group_files"
group_ids = [927825838, 537384511] # i know i am in these groups.
#  import time
check_connection() # failsafe or not?

for group_id in group_ids:
    #  while True:
        #  try:
    group_file_wholesale_downloader(group_id, download_path=download_path, skip_exist=True)
    #  break
        #  except: time.sleep(10) # auto retry.
        # there is no need for any failsafes. maybe we are outside the groups.

# already downloaded. waiting for updates?
