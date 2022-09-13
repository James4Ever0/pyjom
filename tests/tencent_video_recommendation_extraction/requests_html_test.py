from requests_html import HTMLSession # use pyppeteer.
session = HTMLSession()

url='https://www.baidu'

r = session.get(url)