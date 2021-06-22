#!/usr/bin/python

""""
给定一个整数数组和一个目标值，找出数组中和为目标值的两个数
给定一个n长度的数组,返回数组中两个数等于target的索引
example: [2,5,6,9], tagert: 1
return: [0,1]
"""

"""
两层for循环
时间复杂度：O(n*n)
"""
def solution(array, target):
    if len(array)< 2:
        return  array
    for x in range(0, len(array)-1):
        for y in range(x+1, len(array)):
            if array[x] + array[y] ==  target:
                return [x, y]


"""
利用字典hash表, 遍历数组,target-x如果存在，返回对应索引数据
时间负责度： O(n)
"""
def solution2(array, target):
    temp_dict = {}
    result = []
    for index, item in enumerate(array):
        # target - item值
        num =  target- item
        if num not in temp_dict:
            temp_dict[item] = index
        else:
            result.append([index, temp_dict[num]])
    return result

array = [2,5,6,9]
target = 11
print(solution2(array, target))

