# 给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def delNode(head, n):
    # 定义虚拟节点指向head
    dummyHead = ListNode(-1)
    dummyHead.next = head

    fast, slow = head, head
    # 先让快指针指向要删除节点的下一个节点
    for _ in range(n):
        fast = fast.next

    # 快慢指针同时走
    while fast and fast.next:
        fast = fast.next
        slow = slow.next

    # 当快指针走到末尾节点时，慢节点刚好到达要删除的节点的前驱节点
    slow.next = slow.next.next
    return dummyHead.next


