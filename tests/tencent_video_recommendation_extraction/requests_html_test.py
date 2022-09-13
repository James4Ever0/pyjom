from requests_html import HTMLSession # use pyppeteer.
session = HTMLSession()

url='https://www.baidu.com/'

r = session.get(url)
print(r.html.absolute_links)