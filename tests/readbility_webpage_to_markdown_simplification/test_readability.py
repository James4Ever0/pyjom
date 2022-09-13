import requests
from readability import Document

response = requests.get(url)
doc = Document(response.text)
doc.title()