"""
list中的数据类不必相同的，而array的中的类型必须全部相同。
在list中的数据类型保存的是数据的存放的地址，简单的说就是指针
"""
import array
a = array.array("i")
a.append(123)
print(a)

a.append("abc")
print(a)