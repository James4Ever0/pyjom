from bs4 import BeautifulSoup


data = open("dump.html",'r').read()

soup = BeautifulSoup(data)
