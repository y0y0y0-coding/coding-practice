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

        frontier = [root]
        mindepth = 0
        while frontier:
            depth += 1
            next_frontier = []
            for node in frontier:
                if node.left is None and node.right is None:
                    return depth
                if node.left is not None:
                    frontier.append(node.left)
                if node.right is not None:
                    frontier.append(node.right)
            frontier = next_frontier
