from jina import Client, DocumentArray, Document

c = Client(port=12345)
docArray = DocumentArray.empty(1)
        docArray[0].text
r = c.post('/', DocumentArray(Document()))

