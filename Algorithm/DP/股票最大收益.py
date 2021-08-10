# -*- coding: utf-8 -*-
# @Time    : 2021/8/10 9:08
# @Author  : waney
# @File    : 股票最大收益.py

class Solution:
    def maxProfit(self, price_list):

        # 假设第一个值为最小值
        min_price = price_list[0]
        # 最大收益
        max_profit = 0
        for i in range(1, len(price_list)):
            max_profit = max(price_list[i] - min_price, max_profit)
            min_price = min(price_list[i], min_price)
        return max_profit

s = Solution()
print(s.maxProfit([7, 12, 1, 5, 9, 3, 11, 6, 4, 10]))