from bs4 import BeautifulSoup


data = open("dump.html",'r').read()

soup = BeautifulSoup(data)

for elem in soup.find_all(""):
    print(elem)
