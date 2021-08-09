# coding: utf-8

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        # 暴力求解
        # for i in range(len(nums)):
        #     for j in range(i+1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return i,j

        # 哈希表求解
        hash_map = {}
        for index,value in enumerate(nums):  # k: 列表的值   v；列表下标
            if (target-value) not in hash_map:
                hash_map[value] = index
            else:
                return index, hash_map[target-value]


s = Solution()
res = s.twoSum([2,7,6,8], 14)
print(res)