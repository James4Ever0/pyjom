from jina import Client, DocumentArray

if __name__ == '__main__':
    c = Client(host='grpc://0.0.0.0:54321')
    docArray = DocumentArray.empty(1)
    docArray[0].text = input("jina>")
    da = c.post('/', docArray)
    print(da.texts)
