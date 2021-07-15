# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        # 在当前链表前部定义个指针
        head_prev = ListNode(1)
        # 连接起来
        head_prev.next = head

        # 当前指针从头部开始
        curNode = head_prev

        # 开始遍历链表
        while curNode and curNode.next and curNode.next.next:
            f = curNode
            s = curNode.next
            t = curNode.next.next

            # 两两交换链表节点
            # head -> 1 -> 2 -> 3
            f.next = t
            s.next = t.next
            t.next = s
            curNode = curNode.next.next
        return head_prev.next