class User:
    def __init__(self, name, info={}):
        self.name = name
        self.info = info

    # 当查找到实例未有相关属性时，进入该方法
    def __getattr__(self, item):
        # return "not found {}".format(item)
        return self.info[item]

    # 无条件优先进入该方法
    def __getattribute__(self, item):
        return "must inter this func"



if __name__ == '__main__':
    user = User("waney", {"company": "aspire", "address": "shenzhen"})
    # AttributeError: 'User' object has no attribute 'age'
    # not found age
    # print(user.age)
    # print(user.company)