# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 8:50
# @Author  : waney
# @File    : 最大连续子序和.py


"""
定义状态：dp[i] : 以i元素为结尾的最大子序和

dp[i] = max(dp[i-1)+nums[i], num[i])

"""

class Solution:
    def maxSubArray(self, nums) -> int:
        #
        l = len(nums)
        if l <= 0: return 0

        # 定义个n长度的数组
        dp = [0] * l

        # 遍历nums
        for i in range(l):
            dp[i] = max(dp[i-1]+nums[i], nums[i])

        # 返回数组尾部即最大值
        return max(dp)


s = Solution()
print(s.maxSubArray(nums = [-2,1,-3,4,-1,2,1,-5,4]))