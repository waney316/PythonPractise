# 计算从0到n的整数和

# coding: utf-8
def factorial_add(n):
    if n < 1 :
        return 0

    return n + factorial_add(n-1)


res = factorial_add(50)
print(res)



