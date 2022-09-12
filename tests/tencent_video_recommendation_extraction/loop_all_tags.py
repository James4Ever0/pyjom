from bs4 import BeautifulSoup


data = open("dump.html",'r').read()

soup = BeautifulSoup(data)

for elem in soup.find_all():
    # print(elem.attrs)
    # for further examination
    attrs = elem.attrs
    for key in ['src', 'href']:
        if key in attrs.keys():
            print(key, attrs[key])
