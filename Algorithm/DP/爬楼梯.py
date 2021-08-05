# 走楼梯每次只能走一步或2步，有多少种走法
import time
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
res = dict()
def climb_stairs2(n ):
    # 定义数组记录计算过的值
    global  res
    # 当只有一个台阶，仅有一种走法
    if n== 1:
        return 1
    elif n == 2:
        return 2
    res[1], res[2] = 1, 1

    # 如果该值被计算过
    if n in res:
        return res[n]
    else:
        res[n] = climb_stairs(n-1) + climb_stairs(n-2)

    return res[n]


"""
动态规划：
1: 确定状态
2：状态转移方程 f(n) = f(n-1) + f(n-2)

"""
def dp_statirs(n):
    # 记录走法
    if n == 1:
      return 1
    if n == 2:
      return 2
    res = [1, 2]
    for i in range(2, n):
      res.append(res[i - 1] + res[i - 2])
    return res[-1]

if __name__ == '__main__':
    s0_time = time.time()
    r0 = climb_stairs(20)
    print(f"普通递归{time.time() - s0_time}", r0)

    s1_time = time.time()
    r1 = climb_stairs2(20)
    print(f"递归优化{time.time() - s1_time}", r1)

    # s2_time = time.time()
    # r2 = dp_statirs(50)
    # print(f"动态规划{time.time() - s2_time}", r2)
