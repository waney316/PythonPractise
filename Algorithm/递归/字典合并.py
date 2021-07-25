# coding: utf-8

class Solution():
    def __init__(self):
        self.res = {}
        self.key = ""

    def recusorData(self, data):

        for k,v in data.items():
            if isinstance(v, dict):
                self.key = self.key + str(k) + "_"
                return self.recusorData(v)
            else:
                # 最后一层
                res_key = self.key + str(k)
                self.res.update({res_key: v})

        return self.res


def recurNumbers(numbers):
    number_res = []
    if not numbers:
        return []

    for item in numbers:
        if isinstance(item, list):
            number_res.extend(item)
        else:
            number_res.append(item)
    return number_res

if __name__ == '__main__':
    data = {'jack': {'math': {'teacher': 'xxx', 'score': '10'}}}
    numbers = [1, [3, 4], [6, 7, 8], [1,2,3,4,5,6]]  # [1,3,4,5,6,7]

    sl = Solution()
    print(sl.recusorData(data))

    print(recurNumbers(numbers))