# -*- coding: utf-8 -*-
# 快速排序使用分治法（Divide and conquer）策略来把一个序列（list）分为两个子序列（sub-lists）。
"""
从数列中挑出一个元素，称为”基准”（pivot），
重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区结束之后，该基准就处于数列的中间位置。这个称为分区（partition）操作。
递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序。
"""

def quick_sort(array):
    # 定义递归出口
    if len(array) < 1:
        return array

    # 挑选第一个元素作为基准
    pivot = array[0]
    # 比基准大的数列和比基准小的数列
    less, more = [], []

    # 循环数列
    for i in array:
        # 如果当前值比基准小
        if i < pivot:
            less.append(i)
        # 如果当前值比基准大
        elif i > pivot:
            more.append(i)

    # 然后在对less和more进行排序
    less = quick_sort(less)
    more = quick_sort(more)
    # 循环结束后,基准位于两个数列的中间位置
    return less + [pivot] + more


if __name__ == '__main__':
    array = [1,4,3,6,9,2,0,24,15,67,]
    print(quick_sort(array))


