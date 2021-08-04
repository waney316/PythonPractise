# 实现 pow(x, n) ，即计算 x 的 n 次幂函数（即，xn）。

class Solution:
    def myPow(self, x: float, n: int) -> float:
        # for循环求解, 超时
        # sum = 1
        # for i in range(abs(n)):
        #     sum = sum*x
        # return  sum

        # 递归求解

        # 递归出口
        # # 如果幂级数 =0
        # if n == 0:
        #     return 1
        # # 如果幂级数小于0
        # if n < 0:
        #     return 1/self.myPow(x, -n)
        # # 如果幂级数为奇数
        # if n%2:
        #     return x*self.myPow(x, n-1)
        # return self.myPow(x*x, n/2)

        # 递归函数2
        def quickMul(N):
            if N == 0:
                return 1.0
            y = quickMul(N // 2)
            return y * y if N % 2 == 0 else y * y * x

        return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)



