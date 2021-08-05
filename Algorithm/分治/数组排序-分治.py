"""
分治法：

"""

# 冒泡排序
def mp_sort(nums):
    if len(nums) <=1:
        return nums

    # 遍历第一层
    for i in range(len(nums) - 1):
        for j in range(len(nums) - 1 - i):
            if nums[j] < nums[j + 1]:
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


# 归并排序(分治法)
def guibing_sort(nums):
    # 列表一分为2
    mid = int(len(nums)/2)
    res = []
    # 拆分
    left_nums = nums[:mid]
    right_nums = nums[mid:]

    # 分治处理
    if len(left_nums)>1:
        left_nums = guibing_sort(left_nums)
    if len(right_nums) > 1:
        right_nums = guibing_sort(right_nums)

    while left_nums and right_nums:
        # 比较两个数组尾部值
        if left_nums[-1] >= right_nums[-1]:
            res.append(left_nums.pop())
        else:
            res.append(right_nums.pop())
    # 合并
    # res.reverse()
    return (left_nums or right_nums) + res







if __name__ == '__main__':
    li = [7, 5, 0, 6, 3, 4, 1, 9, 8, 2, 12,3,4]

    print(li)
    print(mp_sort(li))
    print(guibing_sort(li))