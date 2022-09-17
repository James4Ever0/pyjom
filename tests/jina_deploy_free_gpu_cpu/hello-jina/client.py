from jina import Client, DocumentArray
# host = 'grpc://0.0.0.0:54321'
# host = 'grpcs://3fcd103a37.wolf.jina.ai'
container_id = '7f015443e8'
host = 'grpcs://{}.wolf.jina.ai'.format(container_id)
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
