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