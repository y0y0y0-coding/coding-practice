from main import Solution, TreeNode


def build_right_skewed_tree(depth: int) -> TreeNode:
    root = TreeNode(0)
    node = root
    for i in range(1, depth):
        node.right = TreeNode(i)
        node = node.right
    return root


if __name__ == "__main__":
    sol = Solution()

    for depth in [10, 900, 1000, 2000]:
        root = build_right_skewed_tree(depth)
        try:
            print(depth, sol.maxDepth(root))
        except RecursionError as e:
            print(depth, "RecursionError:", e)
