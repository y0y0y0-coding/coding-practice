## 問題
- https://leetcode.com/problems/kth-largest-element-in-a-stream/

## メモ（感想や調べたことなど）
### Step.1
- 五分間考えて、わからなかったので回答を確認
- `heapq`を利用している
    - 普通のリストをヒープ(優先度付きキュー)として扱うための関数をまとめたモジュール
- ヒープは「常に最小の要素をすぐ取り出せる」データ構造
- ドキュメント
    - https://docs.python.org/ja/3/library/heapq.html
- 完全二分木のデータ構造
- `h[0](最小値を見る)`:`O(1)`
- `heappush`:`O(log n)`
    - 末尾に追加したあと、親より小さければ入れ替える、を上へ繰り返す
    - 木の高さが`log n`、計算量は`O(log n)`
- `heappop`:`O(log n)`
    - 先頭を取り出し、末尾の要素を先頭に移したあと、子より大きければ入れ替える
    - 木の高さが`log n`、計算量は`O(log n)`
- `heapify`:`O(n)`
    - 下の方の親から順に、各要素を「子より大きければ下へ下ろす」という処理をする。
    - 計算したら`0(n)`になる
- 実装してみたい。
- 回答を読む。
- 上位k個の値をheapに残せば、そのheapの中の最小値が全体でk番目に大きい値になる
- 回答の方のこの表現がわかりやすかった
    - K個入る箱を用意して、溢れなければ入れるだけ、溢れたら入れてとる
- メソッドの仕組み
    - https://docs.python.org/ja/3/tutorial/classes.html#method-objects
    - `メソッドについて特別なこととして、インスタンスオブジェクトが関数の第1引数として渡されます`
    - それを受け取っているのが`self`
        - `self.k`
            - 「インスタンスオブジェクトのk」

```
class KthLargest:

    def __init__(self, k: int, scores: List[int]):
        self.k = k
        self.topk_scores = []
        for score in scores:
            self.add(score)
        
    def add(self, score: int) -> int:
        if len(self.topk_scores) < self.k:
            heappush(self.topk_scores, score)
        else:
            heappushpop(self.topk_scores, score)
        return self.topk_scores[0]
```

- ローカルで実行する形式にすると以下、

```
import heapq

class KthLargest:

    def __init__(self, k: int, scores: list[int]):
        self.k = k
        self.topk_scores = []
        for score in scores:
            self.add(score) 

    def add(self, score: int) -> int:
        if len(self.topk_scores) < self.k:
            heapq.heappush(self.topk_scores, score)
        else:
            heapq.heappushpop(self.topk_scores,score)
        return self.topk_scores[0]

# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, nums)
# param_1 = obj.add(val)
if __name__ == "__main__":
    kth = KthLargest(3, [4, 5, 8, 2])
    print(kth.add(3))   # 期待値 4
    print(kth.add(5))   # 期待値 5
    print(kth.add(10))  # 期待値 5
    print(kth.add(9))   # 期待値 8
    print(kth.add(4))   # 期待値 8
```

### Step.2
- 10分以内に書けるかテスト
    - 初回はテストに失敗した
    - `self.top_k_scores = scores`　の間違いに気が付き修正
    - 10分以内に間違いに気が付き修正はしたが失敗とする   

```
class KthLargest:

    def __init__(self, k: int, scores: list[int]):
        self.k = k
        self.top_k_scores = scores
        for score in scores:
            self.add(score)
                
    def add(self, score: int) -> int:
        if len(self.top_k_scores) < self.k:
            heapq.heappush(self.top_k_scores,score)
        else:
            heapq.heappushpop(self.top_k_scores,score)
        return self.top_k_scores[0]
```

- 再チャレンジ。
    - 10分以内に書けた
    - しかし、`if len(self.top_k_scores) < self.k:` に等号を含めるか？つまり、`self.top_k_scores`の長さがkのときの処理について迷った。
    - 長さがkのとき新たに値を追加してはダメなので、この条件分岐で良い。
    - 今日はここまでとし、明日3回連続で書けるか再チャレンジします

```
import heapq

class KthLargest:

    def __init__(self, k: int, scores: list[int]):
        self.k = k
        self.top_k_scores = []
        for score in scores:
            self.add(score)
            
    def add(self, score: int) -> int:
        if len(self.top_k_scores) < self.k:
            heapq.heappush(self.top_k_scores,score)
        else:
            heapq.heappushpop(self.top_k_scores,score)
        return self.top_k_scores[0]
```

- 3回連続で書けるかを確認。3回目で間違えた。
    - `heapq.heappush(score)`
        - `self.top_kth_scores`を引数にいれていない 
- 翌日、3回連続で書けた

### 他の人のコードを読む
#### 1人目
- https://github.com/Yuto729/leetcode/pull/14/changes のStep.1
    - 配列に数を追加し、`sorted`している
        - `sorted`のドキュメント
            - 時間計算量は O(n log n)
            - 元のリストを変更せず、新しいリストを作って返す
            - `heapq`のソートとはなにが違うのかが気になる
    - `add`は`self.nums = sorted(self.nums + [val], reverse=True)` にまとめられる

```
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = sorted(nums, reverse=True)

    def add(self, val: int) -> int:
        new_sorted_nums = sorted(self.nums + [val], reverse=True)
        self.nums = new_sorted_nums
        return new_sorted_nums[self.k - 1]
```

- 同じ人の次の回答
    - 二分探索
        - 前提として配列はソート済み。今回は降順。
        - `return left`がわからなかったので整理。
            - 目的はvalを入れる位置
            - ループを回しきったら、「....right,left.....」の順になる。
            - valを入れる位置は、rightとleftの間なので、返すindexはleftになる。

```
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = sorted(nums, reverse=True)

    def bin_search(self, val):
        # valが入るindexを変えす.
        left = 0
        right = len(self.nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if val < self.nums[mid]:
                left = mid + 1
            
            elif val == self.nums[mid]:
                return mid
            
            else:
                right = mid - 1
        
        return left
            
    def add(self, val: int) -> int:
        # 2分探索で位置を更新.
        index_to_insert = self.bin_search(val)
        self.nums = self.nums[:index_to_insert] + [val] + self.nums[index_to_insert: ]
        return self.nums[self.k - 1]
```

- 同じ人のStep2
    - 私がみた模範解答はnumsの値を一つずつからに入れていた
    - 今回はnumsを全部入れて、heapソートし、k個まで削っている

```
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.top_k_values = nums
        heapq.heapify(self.top_k_values)
        self._reduce_heapq_length_below_k()

    def _reduce_heapq_length_below_k(self):
        """
        heapqの長さがkより大きいときにk以下まで減らすメソッド
        """
        if len(self.top_k_values) <= self.k:
            return

        while len(self.top_k_values) > self.k:
                heapq.heappop(self.top_k_values)
        
    def add(self, val: int) -> int:   
        heapq.heappush(self.top_k_values, val)
        if len(self.top_k_values) > self.k:
            self._reduce_heapq_length_below_k()
        
        return self.top_k_values[0]
```

- heapqの実装
    - https://github.com/python/cpython/blob/3.14/Lib/heapq.py
    - Pythonで書かれている。
- `heapify`を読んでみる

```
def heapify(x):
    """Transform list into a heap, in-place, in O(len(x)) time."""
    n = len(x)
    # Transform bottom-up.  The largest index there's any point to looking at
    # is the largest with a child index in-range, so must have 2*i + 1 < n,
    # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
    # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
    # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
    for i in reversed(range(n//2)):
        _siftup(x, i)
```

- ソート対象のlistについて、`_siftup`を何回か実行していることはわかる
- `_siftup`を読んでみる

```
def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)
```

- 正直まだ読めていない
- 読んて思ったこと
    - leetcodeの他の人の書いたコードが読みやすいのは、何を解決するためのコードなのかがわかっているから読みやすいのかもしれない。
    - 一旦飛ばして他の人の回答を引き続きみる


#### 2人目
- https://github.com/Satorien/LeetCode/pull/8/changes
    - `insert`使っている。
    - さっきの人は`self.nums[:i] + [val] + self.nums[i:]` 使っていたけどたしかにこれでいけるな

```
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k: int = k
        self.k_largest: List[int] = [None]*k
        while nums:
            self.add(nums.pop())

    def add(self, val: int) -> int:
        for idx in range(self.k):
            if self.k_largest[idx] is None or self.k_largest[idx] < val:
                self.k_largest.insert(idx, val)
                self.k_largest.pop()
                break
        return self.k_largest[-1]
```

#### 3人目
- https://github.com/KaoKao1233/LeetCodeArai60/blob/703_KthLargestElementinaStream/Heap/703_KthLargestElementinaStream/step3.py
- `if len(self.top_k_elements) == k:`なので、numsの要素をすべてチェックしない
- しかし、`nums.sort(reverse=True)` で降順に並び替えているため問題ない

```
import heapq
from typing import List


class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.top_k_elements = []
        nums.sort(reverse=True)

        for num in nums:
            heapq.heappush(self.top_k_elements,num)
            if len(self.top_k_elements) == k:
                break

    def add(self, val: int) -> int:
        heapq.heappush(self.top_k_elements,val)
        if len(self.top_k_elements) > self.k:
            heapq.heappop(self.top_k_elements)
        return self.top_k_elements[0]
```


#### 4人目
- https://github.com/denyaho/Leetcode_repository/blob/kth_heap/kth_largest/step3.py
- 自作の優先度付きキューを実装している
- ` __len__`や`__getitem__` についている`_`アンダーバーは？
    - 特殊メソッド

```
    def push(self, val: int):
        self.queue.append(val)
        idx = len(self.queue) - 1
        while idx > 0:
            parent_idx = (idx - 1) // 2
            if self.queue[parent_idx] <= val:
                break
            self.queue[idx] = self.queue[parent_idx]
            idx = parent_idx
        self.queue[idx] = val
```
- 読めなかったので言語化してみる
    - キューに`val`を追加
    - `idx`
        -　キューの末尾のインデックス
    - `idx`が0以上のときのループ
        - `parent_idx`
            - ~~なぜ1を引いてから2で割っている？~~
            - 親のノードのインデックス。二分木
        - 親ノードとvalの値を比較
            - 親ノードの値がval以下ならループ終了
            - `idx`の値を親ノードの値に置き換え
            - `idx`を親ノードのインデックスにおきかえ
                - このタイミングで親ノードの値を`val`におきかえないでいいのか？
                    - 毎回入れなくても、最後に入れればOK
            - 二分木の最下層から、どこまで上に行けるか
        - ループ終了後の`idx`が示す値に`val`を入れる
    - 読むのにすごい時間がかかってしまった。30分くらい。
        - 具体例を紙に書いて、実際に手を動かしてようやくわかった。

```
    def pop(self) -> int:
        if len(self.queue) == 0:
            return -1
        top = self.queue[0]
        if len(self.queue) == 1:
            self.queue.pop()
            return top
        last = self.queue.pop()
        idx = 0
        while idx * 2 + 1 < len(self.queue):
            left_idx = idx * 2 + 1
            right_idx = idx * 2 + 2
            if right_idx < len(self.queue) and self.queue[right_idx] < self.queue[left_idx]:
                child_idx = right_idx
            else:
                child_idx = left_idx
            if last <= self.queue[child_idx]:
                break
            self.queue[idx] = self.queue[child_idx]
            idx = child_idx
        self.queue[idx] = last

        return top
```

- 次はpopを読んでみる
    - `last`
        - 配列の末尾の値を取得
        - 配列から末尾の値がなくなる
    - `idx`
        - 0からスタート
        - ループでどのように更新される？
    - `while`ループ
        - `left_idx`と`right_idx`は`idx`の子ノードを示す
        - 条件分岐
            - ここで詰まる
            - `if right_idx < len(self.queue) and self.queue[right_idx] < self.queue[left_idx]:`
                - `right_idx < len(self.queue)`
                    - right_idxがキューの長さより大きくなることがあるってこと？？
                - `self.queue[right_idx] < self.queue[left_idx]`
                    - 子ノード同士の値を比較し、小さい方のノードのindexを`child_idx`として取っておく
            - 次に`last`を比較している
                - この処理がわからなかった。
        - `self.queue[idx] = self.queue[child_idx]`
            - 親ノードと子ノードの値を交換
        - `idx`を子ノードのインデックスに更新
            - つまり二分木を下がっていく
            - ここでループの終了条件の意味がわかった。二分木の最下層までいったらstop
        - `right_idx < len(self.queue)`の意味もわかった
            - `left_idx`、左の子ノードがキューの末尾で右の子ノードがないときかな。
        - 最後まで読んだが、以下がわからず
            - 最初に`last｀の値を取得するわけ
            - if last <= self.queue[child_idx]:`

