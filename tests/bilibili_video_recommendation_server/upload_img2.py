url = "https://om.qq.com/image/orginalupload"
# php tencent: http://www.ygbks.com/2501.html gtimg
# python sina: https://www.52pojie.cn/thread-1446200-1-1.html

"""
add something like this in your website
<img src='http://inews.gtimg.com/newsapp_ls/0/14966062446/0' width="200"  referrerpolicy="no-referrer" />
"""
filePath = "test_cover.jpg"
import requests

# with open(filepath, "rb") as f:
#     content = f.read()
# upload elsewhere.
url = "https://om.qq.com/image/exactupload?relogin=1"
picUrl = "https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png"
url = "https://om.qq.com/image/archscaleupload?isRetImgAttr=1&relogin=1"
cookie = {
	"alertclicked": "||",
	"appOmDownClose": "1",
	"csrfToken": "csrf-1666038340355",
	"iip": "0",
	"o_cookie": "917521610",
	"omaccesstoken": "00a8d53ee83b92ec4e3111998ca616ad566b9d6fe80814f1be12d2a5c1e7a267baf531f268514a1be2670c9e98da4549a31b36408ed199c6ccd0e069f62ba65438x0",
	"omtoken": "00a8d53ee83b92ec4e3111998ca616ad566b9d6fe80814f1be12d2a5c1e7a267baf531f268514a1be2670c9e98da4549a31b36408ed199c6ccd0e069f62ba65438x0",
	"pac_uid": "1_917521610",
	"pgv_info": "ssid=s2914806624",
	"pgv_pvid": "977259220",
	"ptcz": "cff0fae128e230ac9cbdca6b44c812da07a8a27199142b3856073da30bd7d37f",
	"ptui_loginuin": "917521610@qq.com",
	"RK": "bNrVuDJjGZ",
	"ts_last": "om.qq.com/userReg/mediaInfo",
	"ts_uid": "6110293192",
	"TSID": "fg2om4ff3b0028rpbovnpafde1",
	"tvfe_boss_uuid": "ba12af7c5a70407c",
	"userid": "22690801",
	"wxky": "1"
}
cookie_str = "; ".join(["{}:{}".format(k, v) for k, v in cookie.items()])
files = {
    "Filedata": open(filePath, "rb"),
    "id": "WU_FILE_0",
    "name": "test_cover.jpg",
    "type": "image/jpeg",
    "lastModifiedDate": "10/18/2022, 4:27:08 AM",
    'appKey':'1',
    'isRetImgAttr':'1',
    'from':'user',
    'subModule':'userAuth_individual_head'
}
req_headers = [
			{
				"name": "Accept",
				"value": "*/*"
			},
			{
				"name": "Accept-Encoding",
				"value": "gzip, deflate, br"
			},
			{
				"name": "Accept-Language",
				"value": "en-US,en;q=0.5"
			},
			{
				"name": "Connection",
				"value": "keep-alive"
			},
			# {
			# 	"name": "Content-Length",
			# 	"value": "197582"
			# },
			# {
				# "name": "Content-Type",
				# "value": "multipart/form-data; boundary=---------------------------26791228924136332743854048233"
			# },
			{ # do some cookie hook to get these data in playwright.
				"name": "Cookie",
				"value": "userid=22690801; omaccesstoken=00a8d53ee83b92ec4e3111998ca616ad566b9d6fe80814f1be12d2a5c1e7a267baf531f268514a1be2670c9e98da4549a31b36408ed199c6ccd0e069f62ba65438x0"
			},
			{
				"name": "Host",
				"value": "om.qq.com"
			},
			{
				"name": "Origin",
				"value": "https://om.qq.com"
			},
			{
				"name": "Referer",
				"value": "https://om.qq.com/userReg/mediaInfo"
			},
			{
				"name": "Sec-Fetch-Dest",
				"value": "empty"
			},
			{
				"name": "Sec-Fetch-Mode",
				"value": "cors"
			},
			{
				"name": "Sec-Fetch-Site",
				"value": "same-origin"
			},
			{
				"name": "User-Agent",
				"value": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
			}
		]
headers = {item['name']: item['value'] for item in req_headers}
respone = requests.post(url, files=files,headers=headers)
res = respone.json()
print(res)


