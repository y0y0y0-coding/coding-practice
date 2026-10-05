## 問題
- https://leetcode.com/problems/two-sum/

## メモ（感想や調べたことなど）
### Step.1
- まず考えたことは単純に虱潰しに調べる方法
- index0を起点に
    - index 1 ~ index lastで条件を満たすものを調べる
- index1を起点に
    - index 2 ~ index lastで条件を満たすものを調べる
- これを最後まで繰り返す。
- リストで一つずつ調べると、計算量が膨大になる
- リスト以外の形で考えられると良さそう。
- ハッシュリストの探索がはやいことを考えると、dictかな。

```
dict = {
    2 : 0,
    7 : 1,
    11 : 2,
    15 : 3
}
```

- これを作っておけば探索はすぐできる。
- 書いてみた

```
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        
        index_to_num = {}
        for idx in len(nums):
            index_to_num[nums[idx]] = idx

        for check_num in index_to_num:
            search_num = target - check_num

            if search_num in index_to_num:
                return [index_to_num[check_num], index_to_num[search_num]]

        
```

- テストまわす。エラー

```
TypeError: 'int' object is not iterable
               ~~~^^^^^^
    for idx in len(nums):
Line 5 in twoSum (Solution.py)
    ret = Solution().twoSum(param_1, param_2)
Line 42 in _driver (Solution.py)
    ~~~~~~~^^
    _driver()
Line 57 in <module> (Solution.py)
```

- `len(nums)`って長さ返すだけ。。
- https://docs.python.org/ja/3/reference/compound_stmts.html#for
- https://docs.python.org/ja/3/builtins/stdtypes.html#range
    - rangeを利用する
    - あとで整理する

```
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        
        index_to_num = {}
        for idx in range(len(nums)):
            index_to_num[nums[idx]] = idx

        for check_num in index_to_num:
            search_num = target - check_num

            if search_num in index_to_num:
                return [index_to_num[check_num], index_to_num[search_num]]

        
```

- テストに失敗
- `nums =[3,2,4]`, `target = 6`の場合は`[0,0]`を返してはいけない。

```
You may assume that each input would have exactly one solution, and you may not use the same element twice.
```

- 条件を追加。

```
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        
        index_to_num = {}
        for idx in range(len(nums)):
            index_to_num[nums[idx]] = idx

        for check_num in index_to_num:
            search_num = target - check_num

            if search_num in index_to_num:
                if index_to_num[check_num] != index_to_num[search_num]:
                    return [index_to_num[check_num], index_to_num[search_num]]
```

- テスト失敗
- `nums =[3,3]`, `target = 6`の場合は`None`を返してしまう。
- `index_to_num`が`{3: 1}`になってしまう。キーが重複しているため。
- dictにそもそもキーが一つしかない。
- returnまでたどりつけず`None`が返ってしまう。
- コメント集にあった、「ジャッジシステムでのレバガチャ」対応をしている。。
- 回答を見る
    - https://github.com/KaoKao1233/LeetCodeArai60/blob/1_TwoSum/HashMap/1_TwoSum/step3.py

```
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}

        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [i, num_to_index[complement]]
            num_to_index[num] = i
```

- dictを作成するアイデアは同じ
- しかし、dictを埋めながら探索している。
- わたしは、一度dictを作成してから探索を始めている
    - しかもキーが重複して作成できていない。。
- 目的は見つけることで、地図作ることではない
- `i`と`complement`がしっくりこなかった。
    - `i`は`idx`にする
    - `complement`は他の候補が思いつかなかったのでそのまま利用する

### Step.2
- 3回連続で10回書けた

```
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        num_to_index = {}

        for idx, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], idx] 
            num_to_index[num] = idx
```

- 他のコード,PRを読む
#### 一人目
- https://github.com/KaoKao1233/LeetCodeArai60/pull/11
- step3のコード以外も読む
- step2
    - https://github.com/KaoKao1233/LeetCodeArai60/blob/1_TwoSum/HashMap/1_TwoSum/step2.py

```
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        sorted_nums = sorted((num, i) for i, num in enumerate(nums)) 
        i = 0
        j = len(sorted_nums) - 1
        sum_val = 0

        while i < j:
            sum_val = sorted_nums[i][0] + sorted_nums[j][0]

            if sum_val == target:
                return [sorted_nums[i][1], sorted_nums[j][1]]
            elif sum_val < target:
                i += 1
            elif sum_val > target:
                j -= 1
```

- `sorted_nums = sorted((num, i) for i, num in enumerate(nums))`
    - `(num, i) for i, num in enumerate(nums)`
        - ジェネレータ式
            - https://docs.python.org/ja/3/reference/expressions.html#generator-expressions 
            - ジェネレータオブジェクトを返す
            - `((num, i) for i, num in enumerate(nums))`
                - ジェネレータオブジェクト
            - `[(num, i) for i, num in enumerate(nums)]`
                - リストを返す
        - リストの内包表記
            - https://docs.python.org/ja/3/tutorial/datastructures.html#list-comprehensions
        - iterable
            - https://docs.python.org/ja/3/glossary.html#term-iterable
            - 反復可能オブジェクトは for ループ内やその他多くのシーケンス
        - タプル
            - https://docs.python.org/ja/3/builtins/stdtypes.html#tuple
            - イミュータブルなシーケンス
        - タブルが要素のsorted: 1つ目の要素で比較
            - `sorted([(3, 0), (1, 1), (2, 2)])`
            - ` [(1, 1), (2, 2), (3, 0)]` 
- このタプルが要素のlistをもとに探索している
    - `i`: numの値が一番小さいタプルからスタート
    - `j`: numの値が一番大きいタプルからスタート
- `i`と`j`のタプルのnumの合計を計算→`sum_val`
- あー、なるほど。`target`と`sum_val`の値の大小を比較して、`i`と`j`を更新しているのか
    - 最初自分は左端から順にみていく発想だったが、ソートして両端同時に見ていくのは面白い

#### 二人目
- https://github.com/Gami19/coding-practice/blob/1_two_sum/1_Two_Sum/step2.py
    - `else`の分岐を書いている
    - また最後の`return`も書いている

```
from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    diff_to_index = {}
    for i, num in enumerate(nums):
        complete = target - num
        if complete in diff_to_index:
            return [i,diff_to_index[complete]]
        else:
            diff_to_index[num] = i
    
    # not found solution
    return []
```

- https://github.com/Gami19/coding-practice/blob/1_two_sum/1_Two_Sum/step1.py
- 私も最初に考えたブルートフォース方式
- 差分が存在したとき、`break`してループを抜けてもよさそう。
    - とおもったけど、`break`しても`i`のループがあるので`return` がいいか。

```
def twoSum(nums: List[int], target: int) -> List[int]:
    """
        ブルートフォース方式：Double Loop
        targetと各要素の差分が0になるものを選ぶ
        ループ j では、スタートをiの次を選ぶことで、重複確認を回避
    """
    n = len(nums)
    # 求める配列
    result = []

    for i in range(n):
        # 差分を定義
        expect = target - nums[i]
        for j in range(i+1,n):
            # 差分が存在する
            if expect == nums[j]:
                result.append(i)
                result.append(j)
    
    return result
```

- https://github.com/Gami19/coding-practice/pull/1#discussion_r3935113683
- 確かに適切かどうかは状況による。わたし最初のブルートフォース方式で書いてみてもよかったかも。

```
適切かどうかは状況によるとは思います。計算量が O(n^2) でも、nが現実的に小さいなら要件によっては普通に走らせても十分に速いこともあるかもしれません。
```

- https://github.com/Gami19/coding-practice/pull/1#discussion_r3969557580
- CPythonの読み残しがわたしもまだたくさんある。dictも読むリストに入れよう

```
気になったタイミングで dictionary （辞書型）のようなデータ構造が一般にどのように実現されているのか調べてみると良いかもしれません。また、CPython における実装を読んでみてもいいかもしれません。
```

#### 三人目
- https://github.com/kanta10250/arai60/pull/1
- https://github.com/kanta10250/arai60/pull/1#discussion_r3887702977
- わたしも最初同じようなことをしていた。 

```
色々な方法がありますが、これはいってみれば、メモ帳を持ちながら、走る方法ですね。

メモを作るために走ってからもう一回走るという方法で書きましたね。別にこれでもいいのですが、一回だけ走るのでもいけませんか?
```

- https://github.com/kazizi55/coding-challenges/pull/10#discussion_r3566068530
    - なぜこの計算量になるのかという考えの道筋が書かれていると嬉しい
    - あとは，計算量だけではなく，実際にどれくらいの時間がかかるのか，という点にも触れられているとなお良いと思います
- わたしは計算量や時間について確認していないので、今後みてみよう
- step4のコードは読みやすかった

#### 四人目
- https://github.com/tsadamor/Leetcode/pull/2/changes#r3607834466
- https://discord.com/channels/1084280443945353267/1201211204547383386/1207251531041210408

```
if の中のほうが、普通ではない、異常な、変わったことが起きて欲しいという感覚ですね。特に return などでは。ただ、趣味の範囲ではあります。
```

- 気にしたことがなかった。自分の感覚ではどうだろう。

```
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {}
        for i, num in enumerate(nums):
            if num not in hash_map:
                hash_map[target - num] = i
                continue
            return [hash_map[num], i]
```

```
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {}
        for i, num in enumerate(nums):
            if num in hash_map:
                return [hash_map[num], i]
            hash_map[target - num] = i
```

- https://github.com/tsadamor/Leetcode/pull/2/changes#r3607819286
- コメントのやりとりの内容が良くわからなかったので調べる
- あくまでLeetcodeではわからないが、解がみつからなかったときなにを返すか。
    - たしかに計算量/実行時間と同じで、仕事として捉えると異常系の処理について考えたほうが良い
- その処理の好みについてのやりとりと理解
    - 空リストを返すより、エラーを返すほうが明示的に解がなかったことがわかりやすくなる
    - なにを返す？
        - そのうえで`raise ValueError`を選んだ理由が書けるとよい
- 組み込み例外のクラス階層
    - https://docs.python.org/ja/3/builtins/exceptions.html#exception-hierarchy

#### Step.3
- 改めて書き直してみる
- 想定される異常系1
    - 解が存在しないとき
        - 何を返す？
- `raise`について
    - https://docs.python.org/ja/3/tutorial/errors.html#raising-exceptions
    - 処理を中断して呼び出し元に例外を伝える
    - 呼び出し元で`except`で受け止めない限り、プログラムはそこで止まる
- `ValueError`
    - https://docs.python.org/ja/3/builtins/exceptions.html#ValueError
    - 入力が問題の前提を満たしていないことを表すエラーは他にはなさそう  
- 想定される異常系2
    - `nums`の要素が文字列の場合
    - 試してみる

```
print(sol.twoSum(["a", "b"], 3))
```

```
$ python3 main.py
Traceback (most recent call last):
  File "/home/y0kun/coding-practice/1_Two_Sum/main.py", line 15, in <module>
    print(sol.twoSum(["a", "b"], 3))
  File "/home/y0kun/coding-practice/1_Two_Sum/main.py", line 6, in twoSum
    complement = target - num
TypeError: unsupported operand type(s) for -: 'int' and 'str'
``` 

- 自分で`raise`を書かなくても、すでに適切な種類の例外で止まる
- 想定される異常系3
    - `nums`がリストでない
- 想定される異常系4
    - `target`が数値でない
- 想定される異常系5
    - `nums`の要素数が0か1
- すべて調べて書いたのが以下

```
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        num_to_index = {}

        for idx, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], idx] 
            num_to_index[num] = idx

        raise ValueError("no pair sums to target!") 

if __name__ == "__main__":
    sol = Solution()

    # 正常系
    print(sol.twoSum([2,7,11,15],9))
    print(sol.twoSum([3,2,4],6))
    print(sol.twoSum([3,3],6))

    # 解が存在しない
    try:
        print(sol.twoSum([1, 2], 10))
    except ValueError as e:
        print("ValueError:", e)

    # nums の要素が数値でない
    try:
        print(sol.twoSum(["a", "b"], 3))
    except TypeError as e:
        print("TypeError:", e)

    # nums がリストでない
    try:
        print(sol.twoSum(None, 3))
    except TypeError as e:
        print("TypeError:", e)

    try:
        print(sol.twoSum(5, 3))
    except TypeError as e:
        print("TypeError:", e)

    # target が数値でない
    try:
        print(sol.twoSum([1, 2], "3"))
    except TypeError as e:
        print("TypeError:", e)

    # 要素数が 0
    try:
        print(sol.twoSum([], 3))
    except ValueError as e:
        print("ValueError:", e)

    # 要素数が 1
    try:
        print(sol.twoSum([3], 3))
    except ValueError as e:
        print("ValueError:", e)
```

- 次は計算量について
    - 入力の長さをNとする
    - 最悪ケースは入力の末尾の値が解のペアの片方
    - `complement in num_to_index`と`num_to_index[num] = idx`が平均`O(1)`
    - よって`O(N)`となる
- 実際に計測してみる
    - `benchmark.py`を作成
- time.perf_counter() 
    - https://docs.python.org/ja/3/library/time.html#time.perf_countero

- benchmark.py

```
import time
from main import Solution

sol = Solution()

for n in [10**4, 10**5, 10**6, 10**7]:
    nums = list(range(n))
    target = (n - 2) + (n - 1)   # 末尾の2つが解になる(最悪ケース)

    start = time.perf_counter()
    sol.twoSum(nums, target)
    elapsed = time.perf_counter() - start

    print(f"n={n}: {elapsed:.6f} 秒")
```

- 実行結果
    - きれいな線形にはならない

```
$ python3 benchmark.py
n=10000: 0.001624 秒
n=100000: 0.015396 秒
n=1000000: 0.197147 秒
n=10000000: 1.692692 秒
```