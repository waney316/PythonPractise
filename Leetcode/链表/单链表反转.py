
class Node:
    def __init__(self, head):
        self.head = head
        self.next = None

"""
思路: 
1:从链表头部节点开始循环,遍历第一个节点时先保存该节点
2:将第一个节点(第一次循环的当前节点)的next为None，及头节点成了None未节点
3:将当前节点赋值给上一个节点
4:将指针从当前节点移到下一个节点
"""

def reverseLinkedList(head):
    # 判断链表是否为空或单个节点
    if head.next is None or not head:
        return head

    # 当前节点和当前节点的前驱节点
    cur = head
    pre = None
    while cur:
        next_node = cur.next
        cur.next = pre
        pre = cur
        cur = next_node
    return pre


if __name__ == '__main__':
    p = Node(1)
    p2 = Node(2)
    p3 = Node(3)
    p.next = p2
    p2.next = p3
    print(p.head, p.next.head, p.next.next.head)

    # 反转
    rp = reverseLinkedList(p)
    print(rp.head, rp.next.head, rp.next.next.head)





