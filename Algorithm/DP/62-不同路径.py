# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 19:21
# @Author  : waney
# @File    : 62-不同路径.py

# 一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为 “Start” ）。
#
# 机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。
#
# 问总共有多少条不同的路径？

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # 定义二维数组
        arr = [[1] * n] + [[1] + [0] * (n - 1) for _ in range(m - 1)]
        for i in range(1, m):
            for j in range(1, n):
                arr[i][j] = arr[i-1][j] + arr[i][j-1]
        return arr[-1][-1]


s = Solution()
print(s.uniquePaths(3,7))