class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def findNode(head, n):
    fast, slow = head, head
    #
    for _ in range(n):
        if fast.next:
            fast = fast.next
        else:
            return None

    while fast:
        fast = fast.next
        slow = slow.next

    return slow


def getKthFromEnd(head, k):
    slow = fast = head
    n = 0
    while fast:
        if n>=k:
            slow = slow.next
        fast = fast.next
        n += 1
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
    p4.next = p5

    print(p1.val, p1.next.val, p1.next.next.val)

    res = findNode(p1, 7)
    print(res)