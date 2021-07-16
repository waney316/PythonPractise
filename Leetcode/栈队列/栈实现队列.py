# coding: utf-8
"""
定义一个输入栈:存储元素
定义一个输出栈：取出元素

"""
class MyQueue(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.input_stack = []
        self.output_stack = []


    def push(self, x):
        """
        Push element x to the back of queue.
        :type x: int
        :rtype: None
        """
        self.input_stack.append(x)


    def pop(self):
        """
        Removes the element from in front of queue and returns that element.
        :rtype: int
        """
        if  not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())

        return self.output_stack.pop()


    def peek(self):
        """
        Get the front element.
        :rtype: int
        """
        if  not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())
        return self.output_stack[-1]


    def empty(self):
        """
        Returns whether the queue is empty.
        :rtype: bool
        """
        return not self.input_stack and not self.output_stack

if __name__ == '__main__':
    q = MyQueue()
    q.push(1)
    q.push(2)
    print(q.peek())

