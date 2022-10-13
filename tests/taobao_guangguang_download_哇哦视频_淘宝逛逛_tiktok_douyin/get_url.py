import requests

s = requests.Session()


parameter="359455393248"
url = 'https://h5api.m.taobao.com/h5/mtop.taobao.content.detail.mix.recommend.h5/1.0/?jsv=2.6.1&appKey=12574478&t=1652513788601&api=mtop.taobao.content.detail.mix.recommend.h5&v=1.0&H5Request=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp3&data=%7B%22contentId%22%3A%22{}%22%2C%22source%22%3A%22guangguang_cainixihuan%22%2C%22pageSize%22%3A5%2C%22pageIndex%22%3A0%2C%22bizParameters%22%3A%22%7B%5C%22itemIds%5C%22%3A%5B%5D%2C%5C%22contentId%5C%22%3A%5C%22{}%5C%22%2C%5C%22videoId%5C%22%3A%5C%22{}%5C%22%7D%22%2C%22extendParameters%22%3A%22%7B%5C%22expoContents%5C%22%3A%5C%22{}%5C%22%2C%5C%22slideAction%5C%22%3A%5C%22up%5C%22%2C%5C%22utparam%5C%22%3Anull%2C%5C%22page%5C%22%3A%5C%22guess-guangguang%5C%22%7D%22%7D'.format(parameter,parameter,parameter,parameter)

s.get(url)
print(s.cookies) # must be valid url then you will be set cookie.
r = s.get(url)

data = r.text

print(data)