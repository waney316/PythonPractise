# coding: utf-8
# 给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

"""
1: 对两个字符串排序 return sorted(s) == sorted(t)
2: 哈希表
"""

class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        s_dict, t_dict = {}, {}

        for i in s:
            s_dict[i] = s_dict[i] +1 if i in s_dict else  1

        for j in t:
            t_dict[j] = t_dict[j]+1 if j in t_dict else 1

        return s_dict == t_dict

s = Solution()
s.isAnagram("abc", "aaaa")


from collections import Counter

counter = Counter("s")
counter.most_common()


