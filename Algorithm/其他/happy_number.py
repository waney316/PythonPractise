# coding: utf-8


# coding: utf-8
# 编写一个算法来判断一个数 n 是不是快乐数。
#
# 「快乐数」定义为：
#
# 对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和。
# 然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。
# 如果 可以变为  1，那么这个数就是快乐数。
# 如果 n 是快乐数就返回 true ；不是，则返回 false 。


def happynumber(num):
    all_set = set()
    while num not in all_set:
        all_set.add(num)
        tmp = sum((map(lambda x: int(x) ** 2, str(num))))
        if tmp ==1:
            return  True
        else:
            num= sum
    return False
