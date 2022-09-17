from jina import Client, DocumentArray
# 'grpc://0.0.0.0:54321'
host = 'grpcs://3fcd103a37.wolf.jina.ai'
if __name__ == '__main__':
    c = Client(host=host)
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
