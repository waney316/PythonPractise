'''
给你一个数组 nums 。数组「动态和」的计算公式为：runningSum[i] = sum(nums[0]…nums[i]) 。
请返回 nums 的动态和。
示例：
输入：nums = [1,1,1,1,1]
输出：[1,2,3,4,5]
解释：动态和计算过程为 [1, 1+1, 1+1+1, 1+1+1+1, 1+1+1+1+1]
'''

class Solution:
    def runningSum(self, nums):
        res = []
        sum = 0
        for n in nums:
            sum = sum+n
            res.append(sum)
        return res

s = Solution()
print(s.runningSum([]))


