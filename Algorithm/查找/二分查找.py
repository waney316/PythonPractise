

# -*- coding: utf-8 -*-

def binary_search(sort_array, val):
    # 如果传入的数组为空值
    if not sort_array:
        return -1

    # 定义开始边界
    beg = 0
    end = int(len(sort_array)-1)
    print(beg, end)
    # 循环边界
    while beg <= end:
        # 找出中间值
        mid = int((beg + end)/2)
        # 如果查找的值大于中间值，那么该值在右半段
        if val > sort_array[mid]:
            # 起始指针指向中间节点
            beg = mid + 1
        elif val < sort_array[mid]:
            end = mid - 1
        else:
            return mid
    return -1


if __name__ == '__main__':
    # sort_array = [1,2,3,4,5,6,7,8]
    # print(binary_search(sort_array, 8))

    def fullpermutation(list):
        if list is None:
            return None
        if len(list) == 1:
            return [list]
        res = []
        pivot = list[0]
        return fullpermutation(list[1:])


    print(fullpermutation([1, 2, 3]))

