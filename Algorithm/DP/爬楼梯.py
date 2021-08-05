# 走楼梯每次只能走一步或2步，有多少种走法

"""
递归运算，其中包含大量重复计算
"""
def climb_stairs(n):
    # 当只有1/2个台阶，仅有n种走法
    if n <= 2:
        return n
    else:
        return climb_stairs(n-1)+climb_stairs(n-2)


"""
递归法，使用数组包含每次计算的点，避免重复计算
"""
def climb_stairs2(n, has_calc):
    # 定义数组记录计算过的值

    # 当只有一个台阶，仅有一种走法
    if n <= 2:
        return n
    else:
        has_calc[n] = climb_stairs(n-1, has_calc) + climb_stairs(n-2, has_calc)
        return has_calc[n]

"""
动态规划：
1: 确定状态
2：状态转移方程 f(n) = f(n-1) + f(n-2)

"""
def dp_statirs(n):
    # 记录走法
    path = []
    if n<2:
        return n
    else:
        i = 3
        for i in range(n):
            path[n] = path[n-1] + path[n-2]
        return path

if __name__ == '__main__':
    print(dp_statirs(4))