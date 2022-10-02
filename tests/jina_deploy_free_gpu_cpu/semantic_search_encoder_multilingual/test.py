from executor import semantic_search_encoder_multilingual
from jina import Flow
import os

if __name__ == "__main__":
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    f = Flow(port=12345).add(uses=semantic_search_encoder_multilingual, replicas=0)

    with f:
        f.block()
