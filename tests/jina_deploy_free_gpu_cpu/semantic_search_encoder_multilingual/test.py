from executor import semantic_search_encoder_multilingual
f = Flow(port=12345).add(uses=semantic_search_encoder_multilingual, replicas=1)

with f:
    f.block()