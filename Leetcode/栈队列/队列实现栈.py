# coding: utf-8
from collections import deque
class MyStack(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        # 定义两个队列
        self.queue = deque()

    def push(self, x):
        """
        Push element x onto stack.
        :type x: int
        :rtype: None
        """

        l = len(self.queue)
        self.queue.append(x)
        for _ in range(l):
            # 将queue里数据放置到从头部放置新的队列
            self.queue.append(self.queue.popleft())


    def pop(self):
        """
        Removes the element on top of the stack and returns that element.
        :rtype: int
        """
        return self.queue.popleft()


    def top(self):
        """
        Get the top element.
        :rtype: int
        """
        return self.queue[0]


    def empty(self):
        """
        Returns whether the stack is empty.
        :rtype: bool
        """
        return not self.queue



# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()