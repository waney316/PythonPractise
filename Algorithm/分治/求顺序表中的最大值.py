# coding: utf-8
# 给定nums
nums = [1,2,3,6,7,10,15]

# 获取元素最大值
def max_nums(nums):
    return max(nums)


def solution(nums):
    # 拆分
    nums_length = len(nums)
    if nums_length < 2:
        return max(nums)

    # left_nums
    left_nums = nums[nums_length//2:]
    rigth_nums = nums[:nums_length//2]

    left_max = solution(left_nums)
    rigth_nums = solution(rigth_nums)

    return max_nums([left_max, rigth_nums])

print(solution(nums))