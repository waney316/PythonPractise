# coding: utf-8

# 递归
def factorial(n):
    if n<=1:
        return 1

    return n*factorial((n-1))

res = factorial(6)
print(res)