# まず自力で解く

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        subarray_max = [0] * len(nums)

        for idx in len(nums):
            if idx == 0:
                continue
            if nums[idx-1] < nums[idx]:
                subarray_max[idx]  = subarray_max[idx-1] + nums[idx]            
            
```

- https://leetcode.com/problems/longest-increasing-subsequence/description/ の要領で書いてみたがだめ
- 言語化してみる
    - 数字が書かれた看板が並んでいる
    - 一番左の看板から歩いて、すべての看板に書かれた数字を確認する
    - 看板に書かれた値を確認し、それまで確認した看板に書かれた合計値を確認する
        - ただし、看板に書かれた値がマイナスだったら、0を記録する
    - 記録した値の中の最大値が答え
- うまく言語化できないが書いてみる

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        subarray_sums = [0] * len(nums)
        subarray_sums[0] = nums[0]

        for idx in range(1, len(nums)):
            if nums[idx] >= 0:
                subarray_sums[idx] = subarray_sums[idx - 1] + nums[idx]

        return max(subarray_sums)
```

- 間違っていたので生成AIに相談

```
「看板の値がマイナスなら 0 を記録する」が違う
捨てるかどうかを決めるのは、今の看板の値ではなく、それまでの合計がマイナスかどうかです。途中にマイナスの看板があっても、それを含めた方が大きくなる場合があります。
また、全部マイナスの場合(例:[-3, -1]、正解は -1)も、記録された 0 が最大になってしまいます。
```
- たしかにマイナスの値があっても、大きくなる場合がある。また、[-3,-1]の場合もだめ
- 書き直してみる
```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        subarray_sums = [0] * len(nums)
        subarray_sums[0] = nums[0]

        for idx in range(1, len(nums)):
            subarray_sums[idx] = max(
                subarray_sums[idx - 1] + nums[idx], subarray_sums[idx]
            )

        return max(subarray_sums)
```
- `[-2,1]`でエラーになる
    - このコードでは`[-2,1]の合計-1が答えになってしまう
- 改めて言語化する
- `subarray_sums[i]`は`i番目の看板で終わる区間の、合計の最大
    - a b c d e と看板がならんでいたら
    - `subarray_sums[2]` は a+b+c、b+c、c の3つの中の最大
    - これをもとめるには？
        - c と 「bで終わる区間 + c 」の比較をする」
            - わたしのコードでまちがっているのはc ではなく、bで終わる区間を比較している
- この探し方で全部の区間をかぞえられている？
    - すべての区間を数えていない。
- `subarray+sums[0]`
    - a
- `subarray+sums[1]`
    - bで終わる区間の最大　= a+bとbで大きい方
- `subarray+sums[2]` 
    - cで終わる区間の最大 = bで終わる区間の最大+c , c で大きいほう
- `subarray+sums[3]` 
- `subarray+sums[4]` 

- 書いてみて通った。

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        subarray_sums = [0] * len(nums)
        subarray_sums[0] = nums[0]

        for idx in range(1, len(nums)):
            subarray_sums[idx] = max(subarray_sums[idx - 1] + nums[idx], nums[idx])

        return max(subarray_sums)
```

- どうやらDPと同じような考えかたらしい。あまりしっくりきてないけど
- 他の人の答えを探している途中に考え方のヒントとなりそうなコメントがあった
- https://discordapp.com/channels/1084280443945353267/1206101582861697046/1207644722491953202

```
まず、 Excel 上で、この問題解けますか? 手で解けないのだと話にならないという感覚があります。
```
- https://discordapp.com/channels/1084280443945353267/1206101582861697046/1207749510797992026
```
んー、一回紙の上でやったほうがいいように思います。

それが終わったらエクセルの上でやってみましょう。

これ、
自分でできる。
やり方を自然言語で説明できる。
コードに変換できる。
コード上の変換で単純化できる。
くらいすると、上のアルゴリズム出てくるはずなんですが、なんとなく、1.2.あたりで引っかかっているように見えています。それにもかかわらず、4.の後を出してきたので、そもそも考え方が違うんじゃないかなと思っています。もうちょっというと、過程が大事なのであって、別に通るコードが書かれることが大事なわけではないです。

O(n^3) で、全部足してみて最大を探す、とか一回手でやってみると、同じことしまくっていて効率悪いなという発想になると思うんですよね。そういうのをすると、まあ、こんなもんでしょうというのを思いつくと思います。あと、全部足してみるのでも、別に3.までやったら効率よくする方法思いつくと思います。
```
- https://discordapp.com/channels/1084280443945353267/1206101582861697046/1208414507735453747

## 他の人のコードを読む
### 1人目
- https://github.com/kazuki-official/leetcode/pull/32/changes
- 初期値をマイナス無限大にしている
- また、配列に答えの候補を保持するのではなく、ループの中で都度最大値を更新している
- これならば空間計算量がO(1)ですむ

```Python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_subarray_sum = float("-inf")
        max_subarray_sum_before = 0
        for num in nums:
            max_subarray_sum_before = max(max_subarray_sum_before + num, num)
            max_subarray_sum = max(max_subarray_sum, max_subarray_sum_before)
        return max_subarray_sum
```

### 2人目
- https://github.com/mamo3gr/arai60/pull/30
- 分割統治法の解き方
- そもそも分割統治法とは？
- ↓生成AI調べ

```
分割統治法は、大きな問題を同じ形の小さな問題に分け、それぞれを解いてから、結果を組み合わせて全体の答えを出す考え方です。

分割:問題を小さく分ける
統治:分けた問題をそれぞれ解く(さらに分けられるなら、また分ける)
結合:小さな答えを組み合わせて、全体の答えにする

分割統治法では分けた小さな問題がそれぞれ独立していて重ならない点です。DP は、同じ小さな問題の答えを何度も使うので「記録して使い回す」ことが効きます。
```

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        def find_max_sum_in_range(left: int, right: int) -> int:
            if left == right:
                return nums[left]

            mid = (left + right) // 2
            left_max = find_max_sum_in_range(left, mid)
            right_max = find_max_sum_in_range(mid + 1, right)
            mid_max = find_max_sum_crossing_mid(left, right, mid)
            return max(left_max, right_max, mid_max)

        def find_max_sum_crossing_mid(left: int, right: int, mid: int) -> int:
            leftward_sum = 0
            left_max = nums[mid]
            for i in range(mid, left - 1, -1):
                leftward_sum += nums[i]
                left_max = max(left_max, leftward_sum)

            rightward_sum = 0
            right_max = nums[mid + 1]
            for i in range(mid + 1, right + 1):
                rightward_sum += nums[i]
                right_max = max(right_max, rightward_sum)

            return left_max + right_max

        return find_max_sum_in_range(0, len(nums) - 1)
```

- `find_max_sum_in_range`は何を返す関数？
    - この問題の答えは、`find_max_sum_in_range(0, len(nums) - 1)`
        - あるidxからあるidxまでのrangeにおけるmax_sumを返す関数
    - どうやってmax_sumを探している？
    - さきほどの分割統治法的な考え
        - left ~ mid のrangeのmax_sum
        - mid + 1 ~ right のrangeのmax_sum
    - ここで突然mid_max、`find_max_sum_crossing_mid`が出てくる
    - これはなに？これがなんで候補になる？
    - わからなっかったので生成AIにきく
- 真ん中をまたぐ区間に答えがある可能性がある
    - 配列を真ん中で左右に分けると、区間は次の3種類のどれかになります。
        - 左半分の中だけにある → left_max
        - 右半分の中だけにある → right_max
        - 左半分と右半分にまたがっている → mid_
- 例:[-1, 3, 4, -1] を [-1, 3] と [4, -1] に分けた場合
    - left_max:左だけの最大 → 3
    - right_max:右だけの最大 → 4
    - mid_max:またぐ区間 3, 4 → 7(これが正解)
- たしかにそう。`find_max_sum_crossing_mid` を読む。
    - 最後に`return left_max + right_max` を返す
    - `left_max`の出し方
        -`leftwarf_sum`がなにを計算しているかわからず。
    - 真ん中をまたぐ区間は分割できる
        - 真ん中から左へ伸ばしたときの区間→最大値がleft_max
        - 真ん中から右へ伸ばしたときの区間→最大値がright_max
- 読むのにすごい時間がかかった。
- この方の最終的な回答

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        cumulated = 0
        max_sum = -math.inf
        for num in nums:
            cumulated += num
            max_sum = max(max_sum, cumulated)
            if cumulated < 0:
                cumulated = 0

        return max_sum
```

- `cumulated`
    - 累積された という意味
- これもKadaneのアルゴリズムで書き方が違うだけ
- なぜcumulatedがマイナスだったら0にリセットしている？
    - 次の看板から数え直すための準備
    - 前の合計を捨てて、この看板1枚から始める
- `max(前の合計 + num, num)` と書き方は違うが、本質的にはおなじ？

### 3人目
- https://github.com/naoto-iwase/leetcode/pull/37

```
  - そこまでの積み重ねのリターンが負の整数分差し引いても上回る場合、跨ぐ価値があると考察した。
  - 一般化して、nums[i]を第i世代の生涯収支とみなし、負になったら子供に相続させるのを取りやめるという例えがはまった。
  - この例えで、（相続分を含めた）財産が最大だった世代の財産を答えればよい。
```

- いろんなイメージの持ち方があり、関心した。
- 私は自分が体を動かすイメージがしっくりくる

## 読みやすく整える
- いまのところの選択肢は
    - 動的計画法
        -Kadaneのかたちにする？
    - 分割統治
- 自分の好みは最初の動的計画法

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        sums_at_end = [0] * len(nums)
        sums_at_end[0] = nums[0]

        for idx in range(1, len(nums)):
            sums_at_end[idx] = max(sums_at_end[idx - 1] + nums[idx], nums[idx])

        return max(sums_at_end)
```

- 直感的に書けるのは上のようなコード
- しかし、配列を使うため空間計算量が`0(n)`になってしまう。
- 配列を使わない書き方にしてみる

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]

        for idx in range(1, len(nums)):
            current_sum = max(max_sum + nums[idx], nums[idx])

        return max_sum

```
- ちょっと見直す。変数の意味を考える
- `current_sum`: 今の看板で終わる区間の最大
    - 初期値：`nums[0]`
    - 更新：`max(current_sum + nums[idx], nums[idx])`
- `max_sum`:これまでの最大の合計
    - 初期値：`nums[0]`
    - 更新：`max(max_sum, current_sumの更新値)`

```Python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]
        current_sum = nums[0]

        for idx in range(1, len(nums)):
            current_sum = max(current_sum + nums[idx], nums[idx])
            max_sum = max(max_sum, current_sum)

        return max_sum

```

- これ配列による記録をする書き方を過程を得ずに、一発で書けるか自信がない

### 時間計算量の見積もり
- 約100万〜1000万steps/秒とする
- `1 <= nums.length <= 10^5` なので、最大step数はそのまま10^5
- 10^5 ÷ (10^6 〜 10^7) = 約 0.01 〜 0.1 秒(10〜100ms 程度


## 時間を測って書き直す
- 三回連続クリア

```Pytnon
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]
        current_sum = nums[0]

        for idx in range(1, len(nums)):
            current_sum = max(current_sum + nums[idx], nums[idx])
            max_sum = max(max_sum, current_sum)

        return max_sum
```

### レビュー依頼
- 実施