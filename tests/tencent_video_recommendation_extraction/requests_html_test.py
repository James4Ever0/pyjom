from requests_html import HTMLSession # use pyppeteer.
session = HTMLSession()

# url='https://www.baidu.com/'
url = ''
r = session.get(url)
for link in r.html.absolute_links:
    print(link)