from jina import Client, DocumentArray, Document

c = Client(port=12345)
r = c.post('/', DocumentArray().add)

