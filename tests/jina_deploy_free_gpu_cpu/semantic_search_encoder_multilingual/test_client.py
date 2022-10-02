from jina import Client, DocumentArray, Document

c = Client(port=12345)
docArray = DocumentArray.empty(1)
docArray[0].text = 'hello world'
docArray[0].data = None
docArray[0].msg = None
r = c.post('/', docArray)
print(r[0])
breakpoint()
# msg = r[0].msg
# if msg == 'success':
#     data = r[0].data
#     print(data)
#     print(data.dtype, shape(data))
# else:
#     print(msg)
#     print("____________ERROR____________")
