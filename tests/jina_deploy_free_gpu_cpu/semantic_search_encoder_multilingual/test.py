from executor import semantic_search_encoder_multilingual
f = Flow(port=12345).add(uses=FooExec, replicas=3).add(uses=BarExec, replicas=2)

with f:
    f.block()