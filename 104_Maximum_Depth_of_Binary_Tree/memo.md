## Step 1 (まずは自分で解く)
- treeのmaximum depthはrootからみた
    - 左の子ノードを頂点とした木のmaximum depth
    - 右の子ノードを頂点とした木のmaximum depth
- の大きい方 + 1 
- 子ノードを頂点とした木のmaximum depthはどうやって求める？
    - `maxDepth`を利用する
- 再帰的な処理で書けそうなので書いてみた

```
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if (root.left is None and root.right is not None):
            return self.maxDepth(root.right) + 1
        if (root.left is not None and root.right is None):
            return self.maxDepth(root.left) + 1
        if (root.left is None and root.right is None):
            return 1

        return max(self.maxDepth(root.left),self.maxDepth(root.right)) +1 
```

- エラー

```
AttributeError: 'NoneType' object has no attribute 'left'
        ^^^^^^^^^
    if (root.left is None and root.right is not None):
Line 10 in maxDepth (Solution.py)
    ret = Solution().maxDepth(param_1)
Line 43 in _driver (Solution.py)
    ~~~~~~~^^
    _driver()
Line 58 in <module> (Solution.py)
```

- `None`が代入されたらエラーが起きる
    - `def maxDepth(self, root: TreeNode | None) -> int:`
- 以下の処理を最初に追加

```
        if root is None:
            return 0
```

- 通るようにはなったが、もっとシンプルに書けそうなので修正する
- `if (root.left is None and root.right is None):`
    - 子ノードを持たないノードの処理
    - `if root is None`で0を返せば、このノードの処理は`return max(self.maxDepth(root.left),self.maxDepth(root.right)) +1` でカバーできている。よって不要

```
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        if (root.left is None and root.right is not None):
            return self.maxDepth(root.right) + 1
        if (root.left is not None and root.right is None):
            return self.maxDepth(root.left) + 1

        return max(self.maxDepth(root.left),self.maxDepth(root.right)) +1
```

- さらに条件分岐をまとめられるか？
- ちょっと考えて思いつかなかったため、生成AIに相談
- 片側だけ子ノードをもつ、場合の処理はいらない
- なぜなら、子ノードがない場合は0を返すので`return max(self.maxDepth(root.left),self.maxDepth(root.right)) +1`でカバーできる

```
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0

        return max(self.maxDepth(root.left), self.maxDepth(root.right)) + 1
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        if root is None:
            return 0
        
        return max(self.maxDepth(root.left),self.maxDepth(root.right)) +1 
        
```

## Step2 (他の人のコードを読み反映)
- 他の人のコードを読む
### 一人目
- https://github.com/Yuto729/leetcode/pull/26/changes
- BFS、DFSでの解いている
    - キュー、スタックにいれるデータは(ノードのアドレス、そのノードのdepth)
- BFSでは`deque()`を利用している
    - 両端から速く出し入れできるデータ構造
    - `Deque はどちらの側からも append と pop が可能で、スレッドセーフでメモリ効率がよく、どちらの方向からもおよそ O(1) のパフォーマンスで実行できます。`
    - `list オブジェクトでも同様の操作を実現できますが、これは高速な固定長の操作に特化されており、基礎のデータ表現形式のサイズと位置を両方変えるような pop(0) や insert(0, v) などの操作ではメモリ移動のために O(n) のコストを必要とします。`
    - 私は別の問題で`queue.Queue()`を利用して書いたが、シングルスレッドの操作では`deque()`のほうが良さそう。
        - https://docs.python.org/ja/3/library/queue.html#queue.Queue
        - `内部的には、これらの3種類のキューは競争スレッドを一時的にブロックするためにロックを使っています; しかし、スレッド内での再入を扱うようには設計されていません。`
- BFSをレベルごとにカウントするコード
    - `frontiers`は同じ深さのノードだけを入れておく
    - `next_frontiers`はその1つ下の深さ
    - ここが読みづらかった。DFSやBFSのように中身を取り出すのではなく、全部書き換えるという発想が個人的にしっくりこなかった
```
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        frontiers = [root]
        depth = 0
        while frontiers:
            depth += 1
            next_frontiers = []
            for node in frontiers:  
                if node.left is not None:
                    next_frontiers.append(node.left)
                if node.right is not None:
                    next_frontiers.append(node.right)
            frontiers = next_frontiers

        return depth
```

### 二人目
- https://github.com/Satorien/LeetCode/pull/21
- 型ヒントをちゃんと書いているのが良いと思った(もしかして`List`は間違い？)。

```
unprocessed_nodes: List[Tuple[TreeNode, int]] = deque([(root, 1)])
```

### 三人目
- https://github.com/fuga-98/arai60/pull/22
- https://github.com/fuga-98/arai60/pull/22#discussion_r1995877168

```
再帰は思っているよりも限界が小さいので、それを念頭に置いて書いてください。
```

- まったく気にしていなかった。調べる

```
再帰呼び出しのたびに、呼び出し途中の情報(どこまで実行したか、ローカル変数など)が積み上がっていきます。際限なく積むとメモリを使い果たしてプログラムが異常終了するので、その手前で止めるための上限です。
```

- 確かに、スタックしていくので大量にメモリを利用してしまう。
- `sys.getrecursionlimit`
    - https://docs.python.org/ja/3/library/sys.html#sys.getrecursionlimit

```
現在の最大再帰数を返します。最大再帰数は、Python インタプリタスタックの最大の深さです。この制限は Python プログラムが無限に再帰し、C スタックがオーバーフローしてクラッシュすることを防止するために設けられています。この値は setrecursionlimit() で指定することができます。
```

- `sys.setrecursionlimit`

```
Python インタプリタの、スタックの最大の深さを limit に設定します。この制限は Python プログラムが無限に再帰し、 C スタックがオーバーフローしてクラッシュすることを防止するために設けられています。
```

- 現在の環境の状況を確認
    - 1000
```
$ python3
Python 3.10.12 (main, Aug 31 2026, 10:18:17) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.getrecursionlimit()
1000
>>>
```

- 深さ1000以上のツリーを作成して、自分の関数が実行されるかテスト
    - ここはズルして生成AIに作成してもらった

```
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
```

- 実行してみた
    - 深さ1000で頭打ちしている。。。

```
$ python3 recursion_limit_test.py
10 10
900 900
1000 RecursionError: maximum recursion depth exceeded
2000 RecursionError: maximum recursion depth exceeded
```

### Step 3 
#### DFSで書き直し
- 自分の書いた再帰のコードを、自分のローカル環境で実行すると深さがたかだか1000以上の木では実行不可になる
- 現実世界では、深さ1000未満の二分木に収まらないデータはある（はず）
- ということで再帰を利用しないBFSやDFSで書き直す方針に切り替える
- DFSで書いてみた

```
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:

        if root is None:
            return 0

        max_depth = 1
        node_stack = [(root, 1)]
        while node_stack:
            current_node, current_depth = node_stack.pop()
            if current_node.left is not None:
                node_stack.append((current_node.left, current_depth + 1))
            if current_node.right is not None:
                node_stack.append((current_node.right, current_depth + 1))
            max_depth = max(max_depth, current_depth)

        return max_depth

```

- なにかしっくりこないので言語化を試みる
- おそらく、子ノードの存在を確認しているのに、わざわざ`current_depth`か確認している点
- 子を持たないノードが`max_depth`の候補になる。
- 子を持たないときに、`max_depth`であるか調べるコードにする

```
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:

        if root is None:
            return 0

        max_depth = 1
        node_stack = [(root, 1)]
        while node_stack:
            current_node, current_depth = node_stack.pop()
            if current_node.left is None and current_node.right is None:
                max_depth = max(max_depth, current_depth)
            if current_node.left is not None:
                node_stack.append((current_node.left, current_depth + 1))
            if current_node.right is not None:
                node_stack.append((current_node.right, current_depth + 1))

        return max_depth
```

#### BFSで書き直し
- `deque`を利用する


```
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:

        if root is None:
            return 0

        max_depth = 1
        node_queue = deque((root, 1))

        while deque:
            current_node, current_depth = node_queue.popleft()
            if current_node.left is None and current_node.right is None:
                max_depth = max(max_depth, current_depth)
            if current_node.left is not None:
                node_queue.append((current_node.left, current_depth + 1))
            if current_node.right is not None:
                node_queue.append((current_node.right, current_depth + 1))

        return max_depth
```

- エラーがおきた

```
TypeError: cannot unpack non-iterable TreeNode object
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    current_node, current_depth = node_queue.popleft()
Line 17 in maxDepth (Solution.py)
    ret = Solution().maxDepth(param_1)
Line 51 in _driver (Solution.py)
    ~~~~~~~^^
    _driver()
Line 66 in <module> (Solution.py)
```

- deque(...) は「イテラブルを受け取り、その中身を1つずつ要素にする
- この作り方だと、`popleft()`で`root`のみ出てくる
- **タプルを1つの要素として入れるには、リストで包んで渡す**
    - 1つの要素として認識させる
    - `node_queue = deque([(root, 1)])`
- `while`の条件式が間違っていたので修正

```
class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:

        if root is None:
            return 0

        max_depth = 1
        node_queue = deque([(root, 1)])

        while node_queue:
            current_node, current_depth = node_queue.popleft()
            if current_node.left is None and current_node.right is None:
                max_depth = max(max_depth, current_depth)
            if current_node.left is not None:
                node_queue.append((current_node.left, current_depth + 1))
            if current_node.right is not None:
                node_queue.append((current_node.right, current_depth + 1))

        return max_depth
```


#### DFSとBFSの書き方のどちらを選ぶか
- イメージとして最深部を探索するDFSのほうが好みなのでDFSで進める
    - 計算量に差がない
    - このような好みで決定していいのだろうか？
- 最終的な回答は以下。
    - 3回連続で10分以内に書けるようになった。

```
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

```