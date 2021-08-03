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
    # onesum维护当前的和
    onesum = 0
    maxsum = nums[0]
    for i in range(len(nums)):
        onesum += nums[i]
        maxsum = max(maxsum, onesum)
        # 出现onesum<0的情况，就设为0，重新累积和
        if onesum < 0:
            onesum = 0
    return maxsum

nums = [-2,1,-3,4,-1,2,1,-5,4]

print(maxSubArray(nums))
print(maxSubArray2(nums))



