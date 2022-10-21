baseUrl = "http://0.0.0.0:5700"

group = 543780931

import requests

url = baseUrl + "/send_group_msg"
payment_urls = [
    "https://qr.alipay.com/tsx10243tdewwaxrvullge8",
    "wxp://f2f0V92qUQI0aBO5PXtWezujxMm-C1KFub6qCi1Obt3cn1KjZqDPqoWKn8ICCcwdt8zU",
]
message = "\n".join(payment_urls)
data = {"group_id": group, "message": message, "auto_escape": False}
r = requests.post(url, data=data)
print(r.json())
# cannot send json. wtf?
# 请参考 go-cqhttp 端输出
