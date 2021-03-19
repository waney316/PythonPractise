# 可迭代对象和迭代器
# 可迭代对象:
from collections.abc import Iterable, Iterator
a = [1,2,3]
print(isinstance(a, Iterable))  # True
print(isinstance(a, Iterator))  # False

iter(a)
print(isinstance(a, Iterator))  # True