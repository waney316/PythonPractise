# 属性描述符
# 场景：初始化类时限制某些属性为特定类型

from numbers import Integral
# 定义属性描述符
class IntField:
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, Integral):
            raise ValueError("Type Error")
        self.value = value

    def __delete__(self, instance):
        pass


class User:
    age = IntField()

if __name__ == '__main__':
    user = User()
    user.age = 30
    print(user.age)
    pass