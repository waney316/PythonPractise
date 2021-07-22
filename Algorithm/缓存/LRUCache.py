# LRU: 最近最少使用算法。使用场景：在有限的空间存储对象时，当空间满时，按照一定的原则删除原有对象

from collections import OrderedDict
from functools import lru_cache

class LRUCache(OrderedDict):
    def __init__(self, size):
        self.cache = OrderedDict()
        # 空间上限
        self.size = size

    def get(self, key):
        # 如果key没有在缓存里，返回-1未找到
        if key not in self.cache:
            return -1
        # 如果在缓存里,表示有使用，取出来放到orderdict尾部
        else:
            # value = self.cache.pop(key)
            # self.cache[key] = value
            self.cache.move_to_end(key)
            return self.cache[key]

    # 更新
    def set(self, key):
        if self.cache["key"]:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) > self.size:
                self.cache.popitem(last=True)
