
class Solution:
    def majorityElement(self, nums) -> int:
        # from collections import Counter
        # count_map = Counter(nums)
        # # 取出出现次数最多的第一个元素
        # return count_map.most_common(1)[0][0]

        # 哈希表求解
        hash_map = {}
        for n in nums:
            if n not in hash_map:
                hash_map[n] = 1
            else:
                hash_map[n] += 1
        print(hash_map)
        max = 0
        for k,v in hash_map.items():
            if v>max:
                max = v
                key = k
        return key





s = Solution()

nums = [2,2,1,1,1,2,2,1,1]
print(s.majorityElement(nums))