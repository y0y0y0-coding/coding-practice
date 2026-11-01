## Step1
- Maximum Depth of Binary Tree とは異なり、minimum depthを調べる
    - https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
- 一段ずつ調べ、そこにleafがあればいいので、BFSが良さそう
- 書いてみた。

```

class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0

        frontier = deque.Queue([(root, 1)])
        while frontier:
            node, depth = frontier.popleft()
            if node.left is None and node.right is None:
                return depth
            if node.left is not None:
                frontier.append((root, depth + 1))
            if node.right is not None:
                frontier.append((root, depth + 1))
```

- エラーがおきた

```
AttributeError: type object 'collections.deque' has no attribute 'Queue'
               ^^^^^^^^^^^
    frontier = deque.Queue([(root, 1)])
Line 12 in minDepth (Solution.py)
    ret = Solution().minDepth(param_1)
Line 45 in _driver (Solution.py)
    ~~~~~~~^^
    _driver()
Line 60 in <module> (Solution.py)
```

- `queue.Queue`と間違えてしまっている。。ドキュメントもっかい読む
- あと、`frontier`に`root`を追加している
- 読むのサボっている。
- 修正して通った。

```
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
```

- 書いてみて思ったことは、`deque`へdepthの値を挿入しなくても良さそう。
- ループした回数を数えたほうが、メモリ効率は良さそう。
- 書いてみた

```
class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0

        frontier = deque(root)
        mindepth = 0
        while frontier:
            node = deque.popleft()
            if node.left is None and node.right is None:
                return mindepth
            if node.left is not None:
                frontier.append(node.left)
            if node.right is not None:
                frontier.append(node.right)
            mindepth += 1
```

- 書いてみたが、`mindepth +=1`を実施するタイミングが良くない
- ループの1周が1段階でなければダメ
- 生成AIと相談しながら直してみる
    - `next_frontier = []` で、毎周新しい空のリストを作る
- 個人的に、読みづらい。おそらく、多重ループが苦手。

```
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

```

## Step2
- 他の人の回答を見てみる

### 1人目
- https://github.com/kazizi55/coding-challenges/pull/22
- 計算量をオーダーに加え、実行時間と空間計算量を算出している。
    - どうやって？
- 10^7:「Python は1秒間に単純な処理をおよそ 10^7 回程度こなせる」という経験則があるらしい（生成AI調べ）
    - 実行時間は自分の環境で測定するのが良さそう
- 推定消費メモリ:10^5 × 8 × 2 / 2 = 800KB
    - `10^5`:ノード数 N
    - `/ 2`:キューに同時に入るのは最大で最下層の N/2 個
    - `× 2`:キューの1要素は (node, depth) の2つの値を持つ
    - `× 8`:64ビット環境で、値への参照1つが 8 バイト
    - ※ただし、タブル自体にも1つあたり数十バイトの管理用の領域がかかる
- `min_depth = sys.maxsize`
    - 64ビット環境で取りうる最大の整数 `2**63 - 1`
    - https://docs.python.org/ja/3/library/sys.html#sys.maxsize
- `nonlocal`
    - 関数の中に定義した関数(内側の関数)から、外側の関数の変数に代入するための宣言
    - https://docs.python.org/ja/3/reference/simple_stmts.html#nonlocal
- 解法3
    - `dataclass`を使う。`dataclass`とは？
        - データを入れておくためのクラスを簡単に書くための仕組み
        - https://docs.python.org/ja/3/library/dataclasses.html

```
from dataclasses import dataclass

@dataclass
class TraverseStatus:
    node: Optional[TreeNode]
    parent_traverse_status: Optional[TraverseStatus] = None
    is_left_child: bool = False
    left_min_depth: int = 0
    right_min_depth: int = 0
    visited: bool = False

class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        traverse_statuses = [TraverseStatus(node=root)]
        while traverse_statuses:
            status = traverse_statuses[-1]
            if not status.visited:
                status.visited = True
                if status.node.left is not None:
                    traverse_statuses.append(
                        TraverseStatus(
                            node=status.node.left,
                            parent_traverse_status=status,
                            is_left_child=True
                        )
                    )
                if status.node.right is not None:
                    traverse_statuses.append(
                        TraverseStatus(
                            node=status.node.right,
                            parent_traverse_status=status,
                        )
                    )
                continue

            traverse_statuses.pop()
            
            if status.node.left is not None and status.node.right is not None:
                min_depth = min(status.left_min_depth, status.right_min_depth) + 1
            elif status.node.left is not None:
                min_depth = status.left_min_depth + 1
            elif status.node.right is not None:
                min_depth = status.right_min_depth + 1
            else:
                min_depth = 1

            if status.parent_traverse_status is None:
                return min_depth

            if status.is_left_child:
                status.parent_traverse_status.left_min_depth = min_depth
            else:
                status.parent_traverse_status.right_min_depth = min_depth
        return 0
```

- 読むのに苦戦。
- ふと思ったけど、さらっと見て頭の中に「わからない」って単語が出てきて、読むの諦めるときがある。。
- メモしながら読んでみる
    - `class TraverseStatus:`に、`is_left_child`は存在するが、`is_right_child`がないのはなぜ？
    - `if not status.visited:`のとき、そのノードの子ノードの情報を取得している。
        - 二回目探索される可能性があるのか？
    - などの疑問を持った
- 改めて読んでみる
    - 最初の`if not status.visited`はスタックの末尾を確認している。
        - popはしていない。
        - そのノードをチェックしていなかったら、スタックに追加する。
    - `traverse_statuses.pop()`でようやくpopする
    - `min_depth = 1`を返している理由がわからなくなった。
- ギブアップして、生成AIの力を借りる
    - そもそもの根本的な考え方が異なっていた。
    - わたしのコードはrootから下へ数えていったが、このコードは葉から上へ数えている
        - 「自分より下の木の最小の深さ」を子から親へ渡していき、根に戻ってきた値が答え
    - `is_left_child`の意味を取り違えていた。自分が左子ノードかどうかである。`is_right_child`がないのも納得
- 読むのに数日かかってしまった。。

```
>>> status = TraverseStatus(node=None)
>>> print(status.__dict__)
{'node': None, 'parent_traverse_status': None, 'is_left_child': False, 'left_min_depth': 0, 'right_min_depth': 0, 'visited': False}
>>> print("Instance base size:", sys.getsizeof(status))
Instance base size: 48
>>> print("Internal dict size:", sys.getsizeof(status.__dict__))
Internal dict size: 296
```

- `__dict__` 特殊属性
    - https://docs.python.org/ja/3/reference/datamodel.html#object.__dict__]
    - インスタンスの属性が辞書形式で出力
- `sys.getsizeof`
    - オブジェクトがメモリ上で使っているバイト数を返す関数
    - https://docs.python.org/ja/3/library/sys.html#sys.getsizeof

### 2人目
- https://github.com/tNita/arai60/pull/21
- `current_depth = max(current_depth, depth)`　はなくてもよさそう。

```Python
class Solution:
    def minDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        frontier = deque()
        frontier.append((root, 1))
        current_depth = 1
        while len(frontier):
            node, depth = frontier.popleft()
            current_depth = max(current_depth, depth)
            if node.left is None and node.right is None:
                return current_depth
            if node.right is not None:
                frontier.append((node.right, current_depth + 1))
            if node.left is not None:
                frontier.append((node.left, current_depth + 1))
        raise RuntimeError("ソースのバグにより最小深さを算出できませんでした。")
```

### 3人目
- https://github.com/skypenguins/coding-practice/pull/16
- テストケースを通過しないコード

```
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        visited_node = deque([root])
        min_tree_depth = 1

        while visited_node:
            node = visited_node.popleft()
            if node.left and node.right:
                min_tree_depth += 1
            if not node.left and not node.right:
                return min_tree_depth
            if node.left:
                visited_node.append(node.left)
            if node.right:
                visited_node.append(node.right)
```

- 動かないのはわかるが、明確に言語化ができなかった。
    - 同じ段に、左右両方に子を持つノードが2つあると、1段なのに +2 される

### Step3
- いくつかのコードを読んだが、自分が最初に書いた上から一段ずつ数えて、子がなかったらその段の深さを返すのが好み
- 上から数えていくほうがわかりやすい
- 最終的な回答

```
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

```