from test_commons import *
from pyjom.main import *

producer = ContentProducer()
producer.main()
print(producer.identifier.data)

reviewer = ContentReviewer()
reviewer.main()
print(reviewer.identifier.data)
