# coding: utf-8

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def delNode(node):
    if not node and node.next is None:
        return None
    # node为当前节点
    nextnode = node.next
    after_nextnode = node.next.next

    node.val = nextnode.val
    node.next = after_nextnode


