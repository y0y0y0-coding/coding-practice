## Step 1
- わからなかったので他の人のコードを読む
    - https://github.com/komdoroid/arai60/pull/14
- まずDFSとBFSについてCloudeに解説してもらう
- DFS
    - 行けるところまで奥へ進み、行き止まりで別の道を試す
    - 主な目的は**全部をたどる**こと
    - スタックを使い実現する。最後にいれたものから取り出す。
- BFS
    - 出発点から近い順に、1段ずつ広げて探索する
    - 主な目的は**最短距離、最短手数**を求める
    - キューを使い実現する
        - `deque`の`append`と`popleft`
- 共通事項
    - 同じ場所を何度も訪れないように、訪問済みを記録する`set`を使うのが一般的
- イメージを掴めたので0から書けるか確認
- 1回目はまったく書けなかった。
- 書く前に、書きたいコードを言語化する
    - 目的は島の数を数えること
        - 「"1"で連結されたもの」の個数を数える
    - 二次元配列のマス(r,c)を確認
        - マス(r,c) が以下の要件を満たしているか？
            - 配列内か？
            - "1"か？
            - 訪れたことがないか？
        - 上記要件を満たしていた場合
            - 訪れたことがない島と判断し、countに+1
            - 訪れたことがあるマスとして記録する
        - 次にマス(r,c)に隣接しているマスを確認
            - 配列内か？
            - "1"か？
            - 訪れたことがないか？
        - すべてを満たしていた場合はさらに
            - 訪れたことがあるマスとして記録する
            - さらに隣のマスを確認する
- 改めて書いてみる

```
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        num_rows = len(grid)
        num_cols = len(grid[0])

        count = 0
        visited = set()
        stack = []
        directions = ((1,0),(-1,0),(0,1),(0,-1))

        for r in range(num_rows):
            for c in range(num_cols):

                if not(0<= r < num_rows and 0 <= c < num_cols):
                    continue
                if grid[r][c] == "0":
                    continue
                if (r,c) in visited:
                    continue

                count += 1
                visited.add((r,c))
                stack.append((r,c))

                while stack:
                    for dx,dy in directions:
                        nei_x = r + dx
                        nei_y = c + dy

                        if not(0<= nei_x < num_rows and 0 <= nei_y < num_cols):
                            continue
                        if grid[nei_x][nei_y] == "0":
                            continue
                        if (nei_x,nei_y) in visited:
                            continue

                        visited.add((nei_x,nei_y))
                        stack.append((nei_x,nei_y))

        return count
```

- Time Limit Exceededで動かないコードが完成した。
- 問題点
    - `while stack`はstackが空になるまで繰り返すが、ループ内で`stack.pop()`していないのでスタックが増える一方
    - `nei_x = r + dx`のように、毎回最初に見つけたマス`(r, c)` の隣を調べている
- 考え方
    - DFSのループ
        - stackから取り出す
        - そのマスの隣を調べる
        - 未訪問ならスタックに積む
- 修正して、無事Accepted

```
        num_rows = len(grid)
        num_cols = len(grid[0])

        count = 0
        visited = set()
        stack = []
        directions = ((1,0),(-1,0),(0,1),(0,-1))

        for r in range(num_rows):
            for c in range(num_cols):

                if not(0<= r < num_rows and 0 <= c < num_cols):
                    continue
                if grid[r][c] == "0":
                    continue
                if (r,c) in visited:
                    continue

                count += 1
                visited.add((r,c))
                stack.append((r,c))

                while stack:
                    x,y = stack.pop()
                    for dx,dy in directions:
                        nei_x = x + dx
                        nei_y = y + dy

                        if not(0<= nei_x < num_rows and 0 <= nei_y < num_cols):
                            continue
                        if grid[nei_x][nei_y] == "0":
                            continue
                        if (nei_x,nei_y) in visited:
                            continue

                        visited.add((nei_x,nei_y))
                        stack.append((nei_x,nei_y))

        return count
```

- コードを整える
- 以下はforの範囲内で満たしているので消す
```
                if not(0<= r < num_rows and 0 <= c < num_cols):
                    continue
```

- 変数の修正
    - 配列に関する変数が混在している。紛らわしいのでそろえたい
        - r,c,row,col
        - x,y
            - xはそもそも列のイメージがある
    - WATER = "0"、LAND = "1"は真似する
    - countもなにを数えているかを明示したい
        - num_islandに変更
    - stack
        - 一般的な名称のためcell_to_visitに変更
- directionsについて
    - https://peps.python.org/pep-0008/#constants

```
Constants are usually defined on a module level and written in all capital letters with underscores separating words. Examples include MAX_OVERFLOW and TOTAL.
```

- モジュールレベルなら定数は大文字で書く
    - モジュールは1つのファイルのことだったので、モジュールレベルは「ファイルの一番外側、つまりクラスや関数の中ではない場所」
- つまり
    - WATER / LAND / DIRECTIONS をclassの外側に書く
    - water / land / directions のローカル変数として、メメソッの外側に書く
- どちらを選ぶか
    - 定数をわかりやすく大文字で書きたいので、classの外側に書いてみる
- if文の条件式をまとめるか？
    - 長すぎて読みづらいので今のままにする

```
if (not (0 <= next_row < num_rows and 0 <= next_col < num_cols)
        or grid[next_row][next_col] == WATER
        or (next_row, next_col) in visited):
    continue
```

- LANDを使ってないので消す
- スペースに関して
    - https://peps.python.org/pep-0008/#whitespace-in-expressions-and-statements
- カンマの後と not の後にスペースを入れるのが一般的
- VS Codeでは、Black Formatterというものがあるので利用する
- https://peps.python.org/pep-0008/#blank-lines
    - PEP 8 の「Blank Lines」の節で、トップレベルの関数やクラスの定義の前後は2行空けると決められている

```
WATER = "0"
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
```

- 比較演算子のスペースも修正された。これもPEP8のルールのもよう
    - https://peps.python.org/pep-0008/#other-recommendations
    - 比較演算子(==、<、<= など)の前後には常にスペースを1つ入れる
- 修正した完成形が以下

```
WATER = "0"
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        num_rows = len(grid)
        num_cols = len(grid[0])

        num_islands = 0
        visited = set()
        cells_to_visit = []

        for row in range(num_rows):
            for col in range(num_cols):

                if grid[row][col] == WATER:
                    continue
                if (row, col) in visited:
                    continue

                num_islands += 1
                visited.add((row, col))
                cells_to_visit.append((row, col))

                while cells_to_visit:
                    cur_row, cur_col = cells_to_visit.pop()
                    for d_row, d_col in DIRECTIONS:
                        next_row = cur_row + d_row
                        next_col = cur_col + d_col

                        if not (0 <= next_row < num_rows and 0 <= next_col < num_cols):
                            continue
                        if grid[next_row][next_col] == WATER:
                            continue
                        if (next_row, next_col) in visited:
                            continue

                        visited.add((next_row, next_col))
                        cells_to_visit.append((next_row, next_col))

        return num_islands

```

- 翌日あらためてコードを書いてみる
- 10分ほどでかけたがエラーがでた

```
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        num_row = len(grid)
        num_col = len(grid[0])

        num_island = 0
        cell_to_visit = []
        visited = set()
        DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        WATER = "0"

        for row in range(num_row):
            for col in range(num_col):

                if grid[row][col] == WATER:
                    continue
                if grid[row][col] in visited:
                    continue

                num_island += 1
                visited.add((row, col))
                cell_to_visit.append((row, col))

                while cell_to_visit:
                    r, c = cell_to_visit.pop()

                    for dy, dx in DIRECTIONS:
                        next_row = r + dy
                        next_col = c + dx

                        if not (0 <= next_row < num_row and 0 <= next_col < num_col):
                            continue
                        if grid[next_row][num_col] == WATER:
                            continue
                        if grid[next_row][num_col] in visited:
                            continue

                        visited.add((next_row, next_col))
                        cell_to_visit.append((next_row, next_col))

            return num_island

```

- エラー内容は以下

```
IndexError: list index out of range
       ~~~~~~~~~~~~~~^^^^^^^^^
    if grid[next_row][num_col] == WATER:
Line 34 in numIslands (Solution.py)
    ret = Solution().numIslands(param_1)
Line 61 in _driver (Solution.py)
    ~~~~~~~^^
    _driver()
Line 72 in <module> (Solution.py)
```

- `num_col`を使っていた。ぱっとみわからなかった
- 他にも`if grid[row][col] in visited` returnの位置がおかしい
- 翌朝、再度書いてみる

```
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        num_rows = len(grid)
        num_cols = len(grid[0])

        num_islands = 0
        cells_to_visit = []
        visited = set()

        WATER = "0"
        DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for row in range(num_rows):
            for col in range(num_cols):

                if grid[row][col] == WATER:
                    continue
                if (row, col) in visited:
                    continue

                num_islands += 1
                visited.add((row, col))
                cells_to_visit.append((row, col))

                while cells_to_visit:
                    r, c = cells_to_visit.pop()
                    for df_r, df_c in DIRECTIONS:
                        next_r = df_r + r
                        next_c = df_c + c

                        if not (0 <= df_r < num_rows and 0 <= df_c < num_cols):
                            continue
                        if grid[row][col] == WATER:
                            continue
                        if (df_r, df_c) in visited:
                            continue

                        visited.add((df_r, df_c))
                        cells_to_visit.append((df_r, df_r))

        return num_islands
```

- 10分ギリギリだった。そしてWrong Answer
    - `next_r`と`next_c`が使われていない。

```
                    for df_r, df_c in DIRECTIONS:
                        next_r = df_r + r
                        next_c = df_c + c

                        if not (0 <= df_r < num_rows and 0 <= df_c < num_cols):
                            continue
                        if grid[row][col] == WATER:
                            continue
                        if (df_r, df_c) in visited:
                            continue
```

- `while cell_to_visit`の処理を書くとき、変数の意味を何も意識せずに書いている自分がいる
- 風を引いて2日ぶりにコードを書いてみたら、スムーズに10分以内に3回書けた
- 次に他の方のコードを読んでみる

## Step 1
### 二人目
- https://github.com/Yuto729/leetcode/pull/22
- この発想は面白いと思った
    - inplaceでvisitedを使わずに解ける. 島番号を定義し, グリッドの各マスを島番号でうめていく.
- forやwhile内のループの変数は`i`や`j`より意味のある単語を使ったほうが好み
- BFS以外にもUnion-Findという解き方がある
- Step3でgridの存在を確認している

```
        if not grid:
            return 0
```

- 初見では`direction`と`directions`を見間違ってしまった。

```
                for direction in directions:
                    neighbor_x = x + direction[0]
                    neighbor_y = y + direction[1]
```

### 三人目
- https://github.com/Satorien/LeetCode/pull/17
- `queue`を使っている
    - https://docs.python.org/ja/3/library/queue.
    - `queue.Queue`
    - `FIFO キューでは、最初に追加されたエントリが最初に取り出されます`
- BFSを読む練習になる
    - DFSとの違いは探索方法の違い
    - BFSはキューにデータを挿入する。そのため、次の探索は最後の入れたデータではなく、キューの先頭にあるデータになる
- `while not to_visit.empty()`
    - `while not to_visit`と書くと常に`True`になる
    - そのため`empty()`メソッドを利用し、評価している。
    - https://docs.python.org/ja/3/builtins/stdtypes.html#truth-value-testing 

```
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def visit_adjacent(i: int, j: int) -> None:
            visited.add((i,j))
            to_visit.put((i - 1, j))
            to_visit.put((i + 1, j))
            to_visit.put((i, j - 1))
            to_visit.put((i, j + 1))
        
        def unfound_land(i: int, j: int) -> bool:
            return grid[i][j] == "1" and (i, j) not in visited

        import queue
        
        visited: Set[Tuple[int]] = set()
        to_visit = queue.Queue()
        island_count: int = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if unfound_land(i, j):
                    island_count += 1
                    to_visit.put((i, j))
                while not to_visit.empty():
                    next_i, next_j = to_visit.get()
                    if not (0 <= next_i < len(grid) and 0 <= next_j < len(grid[i])):
                        continue
                    if unfound_land(next_i, next_j):
                        visit_adjacent(next_i, next_j)
        return island_count
```


### 4人目
- https://github.com/fuga-98/arai60/pull/18
- 再帰を利用したコード。たしかに再帰でも書ける

```
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # 手作業でやるなら、、、縦と横が一緒であれば同じグループっぽい
        # 一つのlandを見つけたら隣接する1を探すか。setに保存していって
        visited = set()

        def search_island(i, j):
            """
            探索済みか海なら0を返却
            landなら隣接するGridすべて探索し、1を返却
            """
            if (i, j) in visited:
                return 0
            if (i < 0 or len(grid) <= i 
                    or j < 0 or len(grid[0]) <= j):
                return 0
            visited.add((i, j))
            if grid[i][j] == "0":
                return 0
            _ = search_island(i + 1, j)
            _ = search_island(i - 1, j)
            _ = search_island(i, j + 1)
            _ = search_island(i, j - 1)
            return 1
        
        result = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                result += search_island(i, j)

        return result
```

- 同じ人のStep3
- `for d_r, d_c in ((0,0),(0,1),(1,0),(-1,0),(0,-1)):` で `(0,0)`が最初わからなかった
    - 探索開始のセルを`visited`にいれる工夫

```
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        LAND = '1'
        num_row = len(grid)
        num_column = len(grid[0])
        visited = set()
        
        def is_new_land(row, column):
            if row < 0 or num_row <= row:
                return False
            if column < 0 or num_column <= column:
                return False
            if grid[row][column] != LAND:
                return False
            if (row, column) in visited:
                return False
            return True

        def traverse(row, column):
            stack = []
            stack.append((row, column))
            while stack:
                stack_r, stack_c = stack.pop()
                for d_r, d_c in ((0,0),(0,1),(1,0),(-1,0),(0,-1)):
                    r = stack_r + d_r
                    c = stack_c + d_c
                    if not is_new_land(r, c):
                        continue
                    visited.add((r,c))
                    stack.append((r,c))

        result = 0
        for row in range(num_row):
            for column in range(num_column):
                if is_new_land(row, column):
                    result += 1
                    traverse(row,column)
        
        return result
```


## BFSで書いてみる
- BFSで書いてみる

```
import queue


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        num_rows = len(grid)
        num_cols = len(grid[0])

        num_islands = 0
        visited = set()
        cell_to_visit = queue.Queue

        WATER = "0"
        DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for row in range(num_rows):
            for col in range(num_cols):

                if grid[row][col] == WATER:
                    continue
                if (row, col) in visited:
                    continue

                visited.add((row, col))
                num_islands += 1
                cell_to_visit.put((row, col))

                while not cell_to_visit.empty:
                    cur_row, cur_col = cell_to_visit.get

                    for df_row, df_col in DIRECTIONS:
                        next_row = cur_row + df_row
                        next_col = cur_col + df_col

                        if not (0 <= next_row < num_rows and 0 <= next_col < num_cols):
                            continue
                        if grid[next_row][next_col] == WATER:
                            continue
                        if (next_row, next_col) in visited:
                            continue

                        visited.add((next_row, next_col))
                        cell_to_visit.put((next_row, next_col))

        return num_islands
```

- エラー

```
TypeError: Queue.put() missing 1 required positional argument: 'item'
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
    cell_to_visit.put((row, col))
Line 26 in numIslands (Solution.py)
    ret = Solution().numIslands(param_1)
Line 64 in _driver (Solution.py)
    ~~~~~~~^^
    _driver()
Line 75 in <module> (Solution.py)
```

- `cell_to_visit = queue.Queue`
    - メソッドを代入してしまっている
    - `()`がない
- あらためて修正

```
import queue


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        num_rows = len(grid)
        num_cols = len(grid[0])

        num_islands = 0
        visited = set()
        cell_to_visit = queue.Queue()

        WATER = "0"
        DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for row in range(num_rows):
            for col in range(num_cols):

                if grid[row][col] == WATER:
                    continue
                if (row, col) in visited:
                    continue

                visited.add((row, col))
                num_islands += 1
                cell_to_visit.put((row, col))

                while not cell_to_visit.empty():
                    cur_row, cur_col = cell_to_visit.get()

                    for df_row, df_col in DIRECTIONS:
                        next_row = cur_row + df_row
                        next_col = cur_col + df_col

                        if not (0 <= next_row < num_rows and 0 <= next_col < num_cols):
                            continue
                        if grid[next_row][next_col] == WATER:
                            continue
                        if (next_row, next_col) in visited:
                            continue

                        visited.add((next_row, next_col))
                        cell_to_visit.put((next_row, next_col))

        return num_islands
```

- 通った。
- 基本的な書き方はDFSと変わらない
- 次に調べる候補をどこからとるかの違い程度だとわかった
- 一応BFSで10分以内に書けるように練習した

## DFSとBFSの計算量について
- Claudeに教えてもらった
- マスの数を N = 行数 × 列数 とします
- 外側のループ:N 個のマスを1回ずつ見る。ほとんどは「水」か「訪問済み」で即スキップ
- 探索(while の中):
    - 起動するのは各島の最初の1マスのときだけで、その島のマスだけを調べる。
    - すべての島の探索を合計しても、取り出されるマスは全体で最大N個
    - 1個取り出すごとに4方向確認するため、最大で4N個
- なので、外側自体の N 回と、while の合計 4N 回を足して N + 4N
- よって時間計算量は`O(N)`
- 最初は`N*4N`と勘違いしていた。
    - 掛け算になるのは、「外側の1回ごとに、内側が毎回フルで回る」場合
    - 積むときに`visited`へ記録しているので、同じマスが2回積まれることはない
    - つまりwhile スタック/キューの処理は毎回実行されない ←ここが躓いたポイント
- 各セルについて処理マックス5回、全部のセルで5回やることはないけど、全体で考えて5Nは超えない 

## 最終的な回答
- DFSとBFSを学びどちらも書けるようになったが、どちらの書き方を選ぶか。
- 計算量が同じなら、リストを使って、シンプルに書けるDFSを最終的な回答とした
    - 他に決めてがない

```
WATER = "0"
DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        num_rows = len(grid)
        num_cols = len(grid[0])

        num_islands = 0
        visited = set()
        cells_to_visit = []

        for row in range(num_rows):
            for col in range(num_cols):

                if grid[row][col] == WATER:
                    continue
                if (row, col) in visited:
                    continue

                num_islands += 1
                visited.add((row, col))
                cells_to_visit.append((row, col))

                while cells_to_visit:
                    cur_row, cur_col = cells_to_visit.pop()
                    for d_row, d_col in DIRECTIONS:
                        next_row = cur_row + d_row
                        next_col = cur_col + d_col

                        if not (0 <= next_row < num_rows and 0 <= next_col < num_cols):
                            continue
                        if grid[next_row][next_col] == WATER:
                            continue
                        if (next_row, next_col) in visited:
                            continue

                        visited.add((next_row, next_col))
                        cells_to_visit.append((next_row, next_col))

        return num_islands

```