# coding: utf-8

# 生成器：包含yeild字段

## 斐波那契数列
def fib(index):
    re_list = []
    n, a, b = 0, 0, 1
    while n<index:
        re_list.append(b)
        a, b = b, a+b
        n += 1
    return re_list
print(fib(10))

# 递归打印斐波那契数列和
def fibfac(index):
    if index < 2:
        return 1
    else:
        return fibfac(index-1)+fibfac(index-2)

print(fibfac(10))


## 生成器
def gen_fib(index):
    n, a, b = 0, 0, 1
    while n<index:
        yield b
        a, b = b, a+b
        n += 1

for item in gen_fib(10):
    print(item)
