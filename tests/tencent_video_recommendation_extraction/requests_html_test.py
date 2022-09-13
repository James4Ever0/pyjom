from requests_html import HTMLSession # use pyppeteer.
session = HTMLSession()

url=''

r = session.get(url)