# coding: utf-8
class Node:
    """定义链表节点"""
    def __init__(self, node):
        # node存放节点元素
        self.node = node
        # next存放下节点元素
        self.next = None

class SingleList():
    def __init__(self):
        # 存放头部
        self._head = None

"""
判断链表是否有环：
1: 定义指定时间time,循环链表,如果链表默认不为None,
2: 循环链表记录每个链表值,使用set去重,如果少于链表长度,有环
3：定义快慢指针,快指针每次走两个元素,慢指针每次走一个元素,如果快慢指针相遇,则有环
"""
# 快慢指针判断链表是否有环
def hasCryleSolution1(linklist):
    # 令快慢指针位于同一起点
    fast, slow = linklist._head, linklist._head
    loopExist = False  #默认没没有环
    # 循环链表,如果node节点存在next 且fast和slow指针不为空
    while fast and fast.next:
        # 快指针指向链表next.next；慢指针指向next
        slow = slow.next
        fast = fast.next.next
        # 如果快慢指针相遇,则有环
        if slow == fast:
            loopExist = True
            break

    # 取出环入口, 从链表头、与相遇点分别设一个指针
    # 每次各走一步，两个指针必定相遇，且相遇第一点为环入口点
    """
    假设链路和环入口长度为len, 环入口距离快慢指针相遇点为x，环长度为r，
    那么慢指针第一次循环时走过的长度为d=len+x，快指针可能绕了n圈，d=len+x+nr ，所以有2d=len+x+nr
    2len+2x = len+x+nr，有len=nr-x, 
    """
    if loopExist:
        fast = linklist._head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        inner = slow.node
        return (loopExist, inner)
    return loopExist

# 使用set判断链表是否有环
def hasCryleSolution2(linklist):
    # 定义set集合
    hashSet = set()
    # 头结点
    node = linklist._head
    loopExist = False
    # 循环链表
    while node:
        if node not in hashSet:
            hashSet.add(node)
        else:
            loopExist = True
            break
        node = node.next

    print(hashSet)
    return loopExist

if __name__ == '__main__':
    # 定义链表节点元素
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)

    # 定义链表
    linklist = SingleList()
    linklist._head = node1
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node3

    # print(linklist.head.node)


    print(hasCryleSolution2(linklist))



