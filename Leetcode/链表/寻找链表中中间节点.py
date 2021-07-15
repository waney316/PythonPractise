class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def findMidNode(head):
    fast, slow = head, head

    # 遍历
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next

    return slow

if __name__ == '__main__':
    p1 = ListNode(1)
    p2 = ListNode(2)
    p3 = ListNode(3)
    p4 = ListNode(4)
    p5 = ListNode(5)
    p1.next = p2
    p2.next = p3
    p3.next = p4
    p5.next = p5


    res = findMidNode(p1)
    print(res.val)