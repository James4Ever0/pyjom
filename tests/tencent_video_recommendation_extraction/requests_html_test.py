from requests_html import HTMLSession # use pyppeteer.
session = HTMLSession()

# url='https://www.baidu.com/'
url = 'http://v.qq.com/x/page/m0847y71q98.html'
r = session.get(url)
for link in r.html.absolute_links:
    print(link)