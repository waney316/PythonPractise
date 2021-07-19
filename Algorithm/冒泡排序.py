# -*- coding: utf-8 -*-

# 冒泡排序：时间复杂度 O(n*n)

def bubble_sort(array):
    # 如果数组为空或者数组长度为
    if len(array) < 1:
        return array

    # 获取数组长度
    length = len(array)

    # 双层for循环
    for i in range(0, length):
        for j in range(i+1, length):
            if array[i] > array[j]:
                temp = array[j]
                array[j] = array[i]
                array[i] = temp

    return array


if __name__ == '__main__':
    array = [1,4,3,6,9,2,0,24,15,67,]
    print(bubble_sort(array))
