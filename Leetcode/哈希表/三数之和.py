# coding: utf-8
# 给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有和为 0 且不重复的三元组。
#

class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        # 三层循环
        # res = []
        # for x in range(len(nums)):
        #     for y in range(x+1, len(nums)):
        #         for z in range(y+1, len(nums)):
        #             if nums[x] + nums[y] +nums[z] ==0:
        #                 res.append(sorted([nums[x], nums[y], nums[z]]))
        #
        # return [list(t) for t in set(tuple(_) for _ in res)]

        # 两层循环
        # hash_map = {}
        # res = []
        # for a in range(len(nums)):
        #     for b in range(a+1, len(nums)):
        #         if -(a+b) not in hash_map:
        #             hash_map[-(a+b)] = [nums[a], nums[b]]
        #         else:
        #             res.append([nums[a], nums[b], nums[-(a+b)]])
        # return res


        # 先排序在超找
        if not nums or not nums[0]:
            return  []
        res = []
        sort_nums = sorted(nums)  # logn
        start = 2
        end = len(nums)
        print(sort_nums)
        for index,value in enumerate(sort_nums):

            if sort_nums[index] + sort_nums[start] + sort_nums[end] <0:
                end = end - 1
            elif sort_nums[index] + sort_nums[start] + sort_nums[end] >0:
                start = start + 1
            elif sort_nums[index] + sort_nums[start] + sort_nums[end] ==0:
                res.append([sort_nums[index], sort_nums[start], sort_nums[end]])
        return res


nums = [-1,0,1,2,-1,-4]

s = Solution()
print(s.threeSum(nums))


