from jina import Client, DocumentArray

if __name__ == '__main__':
    c = Client(host='grpc://0.0.0.0:54321')
    while True:
        docArray = DocumentArray.empty(1)
        docArray[0].text = command = input("jina> ")
        if command == 'exit':
            print('exiting jina')
            break
        da = c.post('/', docArray)
        response = da[0].text
        # print(da.texts)
        print(response)
