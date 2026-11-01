from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0

        frontier = deque([(root, 1)])
        while frontier:
            node, depth = frontier.popleft()

            if node.left is None and node.right is None:
                return depth
            if node.left is not None:
                frontier.append((node.left, depth + 1))
            if node.right is not None:
                frontier.append((node.right, depth + 1))
