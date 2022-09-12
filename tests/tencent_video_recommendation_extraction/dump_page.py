from playwright.sync_api import sync_playwright

def run(playwright):
    webkit = playwright.webkit
    browser = webkit.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://v.qq.com/x/page/m0847y71q98.html")
    content = page.content()
    with open("dump.html", 'w+') as f: f.write(content)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
