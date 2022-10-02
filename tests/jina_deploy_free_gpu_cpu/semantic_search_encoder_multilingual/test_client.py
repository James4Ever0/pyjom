from jina import Client, DocumentArray, Document

c = Client(port=12345)
docArray = DocumentArray.empty(1)
docArray[0].text = 'hello world'
r = c.post('/', docArray)

print(r[0])
