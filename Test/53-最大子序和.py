#
# 输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
# 输出：6
# 解释：连续子数组 [4,-1,2,1] 和最大，为6

def maxSubArray(nums):
    res = nums
    # 遍历nums数组
    for i in range(1, len(nums)):
        max_number = max(nums[i], nums[i] + nums[i-1])
        res[i] = max_number
    return max(res)


def maxSubArray2(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    # 如果数组长度小于1
    if len(nums)<1:
        return nums[0]
    max = 0
    # i,j 指针遍历
    for i in range(0, len(nums)):
        for j in range(i+1, len(nums)+1):
            temp = sum(nums[i:j])
            if temp > max:
                max = temp
    return max

nums = [-2,1,-3,4,-1,2,1,-5,4]


# print(maxSubArray(nums))
print(maxSubArray2(nums))



