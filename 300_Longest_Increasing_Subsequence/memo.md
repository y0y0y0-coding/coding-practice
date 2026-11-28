## まず自力で解く
- https://leetcode.com/problems/longest-increasing-subsequence/
- 単純に考えると、
    - 配列の特定のindexを起点として、それ以降のindexで、起点としたindexより大きい値がいくつあるか数える
    - 左から数えてすべてのindexを起点としたパターンを調べる
    - 効率が悪い。同じ比較を重複している。別の方法を考える。
- 別の方法を考える
    - 配列の左からではなく、右から数えていけばよい？   
        - `nums = [10,9,2,5,3,7,101,18]` なら
            - 18を起点：1
            - 101を起点
                - 18と比較
            - 7を起点
                - 101と比 
- うまくいかず。回答をみる
- 参考にした回答
    - https://github.com/Hiroto-Iizuka/coding_practice/pull/31/changes

```
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        subsequences = [1] * len(nums)

        for idx in range(len(nums)):
            for pre_idx in range(idx):
                if nums[idx] > nums[pre_idx]:
                    subsequences[idx] = max(subsequences[pre_idx] + 1, subsequences[idx])

        return max(subsequences)
```

- 考え方のイメージ
    - 人が一列に並んでいる。自分と自分より左に並んでいる人たちで背の順の列を作る
        - 左に並んでいる人たちも同じことをしてるので、その値を参考にさせてもらう
            - 自分より背が小さい人がいたら、その人の作った列の末尾に自分が加われば良い
            - 自分より左に並んでいる人、全員と背比べして最長になる値を記録する
- 時間計算量の見積もり
    - `O(N^2), Nはnumsの長さ`
    - 制約では`nums.length`の最大は2500なので、大雑把に2500^2 = 6 × 10^6
    - Python: 約100万〜1000万steps/秒と考えると、6 × 10^6 ÷ (10^6 〜 10^7) = 約 0.6 〜 6 秒


## 読みやすく整える
- `subsequences` という変数に違和感を感じる
- このリストには部分列が入っているのではなく、「`idx`の値で終わる最長の長さ」
- 他の人のレビューをみる
    - https://github.com/attractal/leetcode/pull/10#discussion_r3014968656
    - シンプルに`max_lengths`がいいかな？
- 他の人のコードをもっと読んでみる


### 他の人のコードを読む
#### 1人目
- 貪欲法 ＋ 二分探索のコード
    - https://github.com/skypenguins/coding-practice/pull/50/changes

```
class Solution:
    def lengthOfLIS(self, nums):
        tails = []
        for num in nums:
            pos = bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        return len(tails)
```

- `bisect_left`
    - https://docs.python.org/ja/3/library/bisect.html#bisect.bisect_left
    - ソートされた順序を保ったまま`num`を`tails`に挿入できる点を探す
- `tails`は何を表している？
    - `tails[k]` は「長さ`k+1`の増加部分列の、末尾にできる最小の数」
        - `tails[0]`は長さ1の増加部分列の末尾にできる最小の数
        - `tails[1]`は長さ2の増加部分列の末尾にできる最小の数
        - `tails[2]`は長さ3の増加部分列の末尾にできる最小の数
        - `tails[3]`は長さ4の増加部分列の末尾にできる最小の数
- 最初に書いたコードと発想が全然違う
    - 最初に書いたコードは、その人が列の末尾に参加したときの部分配列の最長の長さ
- 今回は、
    - 自分が一番背が高かったら、一番長い列の後ろに乗っかれるので、新しい枠ができてそこに立つ
    - 同じ長さの列を、より低い最後尾で作れるので交代する
- `bisect_left`、二分探索の時間計算量は`O(log N)`なので、最初に見たコードより早い
    - 1回比べるたびに、探す範囲が半分になるので、`N → N/2 → N/4 → … → 1`のステップ数が`log N`

#### 2人目
- https://github.com/shining-ai/leetcode/pull/31
- `数直線で考えたとき、右側が大きくなるよう、 nums[j] < nums[i] としたいです。あるいは`
    - たしかに左からチェックしているので、このほうが自然そう
- `セグメントツリーと座標圧縮を使うのは、この問題を解くにあたっては指し過ぎだと思います。勉強のためと割り切って書くのは良いと思います。`
    - セグメントツリーも座標圧縮もきいたことないので、参考程度に読んでみる
    - ソフトウェアエンジニアの常識の範囲には、ぎりぎり入っていなそうとのこと。
- 座標圧縮
    - 値の大きさそのものは捨てて、小さい順の順位に置き換えること
    - `[100, -5, 30]  →  [2, 0, 1]`
- セグメントツリー
    - リストの「ある範囲の最大値」(合計などの場合もあります)を、`O(log n)`ですばやく求められるデータ構造

#### 3人目
- https://github.com/attractal/leetcode/pull/10/changes
- 同じく貪欲法でといている。

### 自分のコードを整える
- 貪欲法 ＋ 二分探索のコードか最初の回答で迷ったが、最初の回答を選択する
    - 個人的に直感的で読みやすいため
    - 仕事と考えるとこのような理由で選んでいいのだろうか。。？
- 最終的な回答

```Python
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        max_length = [1] * len(nums)

        for idx in range(len(nums)):
            for pre_idx in range(idx):
                if nums[pre_idx] < nums[idx]:
                    max_length[idx] = max(max_length[pre_idx] + 1, max_length[idx])

        return max(max_length)
```

## 時間を測って書き直す
- 10分以内に一度もエラーを出さずに書けるようになるまで繰り返すを3回連続成功。