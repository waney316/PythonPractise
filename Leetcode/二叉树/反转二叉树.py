# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        # 递归出口
        if not root:
            return root

        # 交换节点
        root.right, root.left = root.left, root.right

        # 递归反转左节点和右节点
        self.invertTree(root.right)
        self.invertTree(root.left)
        return root