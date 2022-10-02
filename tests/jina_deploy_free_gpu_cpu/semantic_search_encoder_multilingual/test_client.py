from jina import Client, DocumentArray, Document

c = Client(port=12345)
docArray = DocumentArray.empty(1)
docArray[0].text = 'hello world'
r = c.post('/', docArray)
msg = r[0].msg
if msg == 'success':
    print(r[0].data)
    print(r[0].data.dtype, shape(data))
