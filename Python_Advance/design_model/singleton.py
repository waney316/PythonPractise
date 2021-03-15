# # -*- coding: utf-8 -*-
#
# '''
# 一般类定义
# '''
# class A:
#     def __init__(self):
#         pass
#
#
# class B:
#     def __init__(self):
#         pass
#
# a = A()
# b = B()
# print(a)
# print(b)


'''
使用__new__方法
'''
# class Base(object):
#     def __new__(cls, *args, **kwargs):
#         # 如果当前类没有实例化对象
#         if not hasattr(cls, "_instance"):
#             cls._instance = super().__new__(cls, *args, **kwargs)
#         return cls._instance
#
#
# d1 = Base()
# d2  =Base()
# print(d1)
# print(d2)

'''
使用装饰器
'''
# def singleton(cls, *args, **kwargs):
#     _instance = None
#     def get_instance(*args, **kwargs):
#         nonlocal _instance
#         if _instance is None:
#             _instance = cls(*args, **kwargs)
#         return _instance
#     return get_instance
#
#
# @singleton
# class Foo(object):
#     def __init__(self):
#         self.name = "foo"
#
# f1 = Foo()
# f2 = Foo()
# print(f1)
# print(f2)


'''
使用元类
'''
class SingleTonType(type):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        _instance = None  # 设置一个变量，用来存储是否创建实例
        print('cls:',cls)
        if _instance is None:
            obj = cls.__new__(cls,*args, **kwargs)  # 会一直找到能创建实例的父类，创建实例
            cls.__init__(obj, *args, **kwargs) # 构造方法去丰富该实例
            cls._instance = obj   # 并将变量修改的创建的实例
        return _instance

class Foo(metaclass=SingleTonType):
    def __init__(self,name):
        self.name = name

if __name__ == '__main__':
    obj1 = Foo('hello')  # 会调用type类（SingleTonType）中的call方法
    obj2 = Foo('world')
    print(id(obj1), id(obj2))