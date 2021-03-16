class Demo():
    def __init__(self, students):
        self.students = students

    def __getitem__(self, item):
        return self.students[item]
# 常规遍历方法
d = Demo(["tom", "waney", "hah"])
# for stu in d.students:
#     print(stu)
# # 通过__get_item__方法
# for stu in d:
#     print(stu)

'''__str__'''
class Test():
    def __init__(self):
        self.name = "测试"

    def __str__(self):
        return self.name
    def __repr__(self):
        print(self.name)
t = Test()
print(t)





