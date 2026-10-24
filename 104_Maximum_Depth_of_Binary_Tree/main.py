from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0

        maxdepth = 0
        nodes = [(root, 1)]

        while nodes:
            node, depth = nodes.pop()

            if node.left is None and node.right is None:
                maxdepth = max(maxdepth, depth)
            if node.left is not None:
                nodes.append((node.left, depth + 1))
            if node.right is not None:
                nodes.append((node.right, depth + 1))

        return maxdepth
