"""
分治法：

"""

# 冒泡排序
def mp_sort(nums):
    if len(nums) <=1:
        return nums

    # 遍历
    for i in range(len(nums) - 1):
        for j in range(len(nums) - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]

    return nums






# 快速排序
def part_sort(nums):
    if len(nums)<1:
        return []
    # 取出一地个数作为基准
    privot = nums[0]
    # 大于基准的数
    more_privot_nums = [n for n in nums[1:] if n > privot]
    # 小于基准的数
    less_privot_nums = [n for n in nums[1:] if n < privot]
    # 递归合并
    return part_sort(more_privot_nums) + [privot] + part_sort(less_privot_nums)


if __name__ == '__main__':
    lis = [7, 5, 0, 6, 3, 4, 1, 9, 8, 2, 12,3,4]
    print(mp_sort(lis))