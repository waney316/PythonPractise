# 编写代码，移除未排序链表中的重复节点。保留最开始出现的节点。

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def delMutiNode(head):
    if not head:
        return head

    r = head
    record = {head.val}
    while r and r.next:
        if r.next.val not in record:
            record.add(r.next.val)
            r = r.next

        else:
            r.next = r.next.next
    return record

if __name__ == '__main__':
    p1 = ListNode(1)
    p2 = ListNode(2)
    p3 = ListNode(3)
    p4 = ListNode(3)
    p5 = ListNode(5)
    p1.next = p2
    p2.next = p3
    p3.next = p4
    p4.next = p5

    res = delMutiNode(p1)
    print(res)


