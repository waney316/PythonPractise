from collections.abc import Mapping, MutableMapping

# dict 属于Mapping

a = {}
print(isinstance(a, Mapping))

a = dict()
a.items()