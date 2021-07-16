class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        # 定义一个湛
        stack = []

        strMap = {")": "(", "}": "{", "]": "[" }
        for item in s:
            if item not in strMap:
                stack.append(item)
            elif not stack or strMap[item] != stack.pop():
                return False

        return not stack


if __name__ == '__main__':
    s = Solution()
    print(s.isValid("}})"))