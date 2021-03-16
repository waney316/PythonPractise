# 列表生成式
# 1：提取1-20之间的偶数
odd_list = []
for i in range(1,21):
    if i%2 == 0:
        odd_list.append(i)
print(odd_list)
# 列表生成式
l = [ i for i in range(1,21) if i%2==0]
print(l)

## 生成器表达式
g = (i for i in range(1,21) if i%2==0)
print(type(g))
print(g)
for item in g:
    print(item)

## 字表推导式
dict = {"name":  "wangwei", "age": 24, "address": "深圳", "address2": "深圳"}
odd_dict = {v:k for k,v in dict.items()}
print(odd_dict)

# 集合推导式
my_set = {value for value in dict.values()}
print(my_set)


