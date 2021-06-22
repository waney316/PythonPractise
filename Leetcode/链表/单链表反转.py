class Node:
    """定义链表节点"""
    def __init__(self, node):
        # node存放节点元素
        self.node = node
        # next存放下节点元素
        self.next = None

"""
思路: 
1:从链表头部节点开始循环,遍历第一个节点时先保存该节点
2:将第一个节点(第一次循环的当前节点)的next为None，及头节点成了None未节点
3:将当前节点赋值给上一个节点
4:将指针从当前节点移到下一个节点
"""
def reverseLinkList(linklist):
    # 判断链表是否为空或单节点
    if linklist is None or linklist.next is None:
        return linklist
    # 当前指针
    cur_node = linklist
    pre_node = None
    while cur_node is not None:
        # 临时保存当前节点
        next_node = cur_node.next
        # 将当前节点的下一节点为None
        cur_node.next = pre_node
        # 上一节点为当前节点
        pre_node = cur_node
        # 指针移到下一节点
        cur_node = next_node
    return pre_node


if __name__ == '__main__':
    Llist = Node(1)
    p2 = Node(2)
    p3 = Node(3)

    Llist.next = p2
    p2.next = p3

    print(Llist, Llist.next, Llist.next.next, )
    reverse_list = reverseLinkList(Llist)
    print(reverse_list, reverse_list.next, reverse_list.next.next, )



