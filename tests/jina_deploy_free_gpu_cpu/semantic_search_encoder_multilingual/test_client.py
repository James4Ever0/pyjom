from jina import Client, DocumentArray, Document

c = Client(port=12345)
docArray = DocumentArray.empty(1)
docArray[0].text = 'hello world'
r = c.post('/', docArray)
r_0 = r[0]
# print(dir(r_0))
# print(r_0.tags)
# breakpoint()
text = r[0].text
if text == 'success':
    data = r[0].embedding
    print(data)
    print(data.dtype, shape(data))
else:
    print(text)
    print("____________ERROR____________")
