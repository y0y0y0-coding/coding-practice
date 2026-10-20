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
        node_to_visit = [(root, 1)]

        while node_to_visit:
            current_node, current_depth = node_to_visit.pop()

            if current_node.left is None and current_node.right is None:
                maxdepth = max(maxdepth, current_depth)
            if current_node.left is not None:
                node_to_visit.append((current_node.left, current_depth + 1))
            if current_node.right is not None:
                node_to_visit.append((current_node.right, current_depth + 1))

        return maxdepth
