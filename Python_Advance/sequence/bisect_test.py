# coding: utf-8
"""
bisect: 排序模块

"""

import bisect
test = [1, 2, 6, 8, 19]
position = bisect.bisect(test, 8)
print(position)

position_left = bisect.bisect_right(test, 6)
print(position_left)

bisect.insort(test, 6)
print(test)