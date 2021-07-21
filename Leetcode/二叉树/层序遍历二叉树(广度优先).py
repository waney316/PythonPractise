# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        # 如果根节点，返回为空
        if not root:
            return []

        # 将跟节点存入队列
        queue = [root]
        # 存储遍历结果
        res = []
        # 开始从跟节点遍历
        while queue:
            # 将当前节点额值存入队列
            res.append([node.val for node in queue])

            # 开始遍历queue
            nodes = []
            for q in queue:
                if q.left:
                    nodes.append(q.left)
                if q.right:
                    nodes.append(q.right)

            # 将指针移到nodes
            queue = nodes
        return res

