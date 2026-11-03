# coding-practice

コーディング練習会の取り組み用リポジトリ

## 取り組む問題

[LeetCode 定番問題リスト](https://1kohei1.com/leetcode/)

## 言語

Python3

## リポジトリの使い方

- 問題ごとにブランチを切る (例: `two-sum`)
- 解答を書いてプッシュし、GitHub 上で Pull Request を作成する
- PR にいただいたコメントを反映し、必要に応じて修正をプッシュする

## 進め方

進め方の自由度は高く、以下に固定する必要はない。代表的な型として記録しておく。

### 問題の選び方

- [新井康平さんの問題集](https://1kohei1.com/leetcode/) を使う人が多い。番号順より、カテゴリごとに一周する方がおすすめ
- AtCoder や ICPC の問題を使う人もいる
- 上記が難しい場合は [learnpython.org](https://www.learnpython.org/) から始めるのもよい
- 過去に同じ問題を解いた人がいると、その人からコメントをもらいやすい

### 基本サイクル（目安5段階）

1. **まず自力で解く**
    - 答えを見ずに考える。5分考えて分からなければ答えを見る
    - 答えを見て理解したら、答えを隠して自分で書く。筆が進まず5分迷ったら再度答えを見て、見たら全部消してやり直す
    - Accept されたら1段階目クリア
2. **読みやすく整える**
    - 動くコードを、変数名や条件分岐などを整理して読みやすくする。整ったら2段階目クリア
    - 過去に同じ問題を解いた人のコードとレビューコメントを読む。書くより他人のコードを読む方が学習効果が高い。レビューコメントを予測してみるとよい学習になる
3. **時間を測って書き直す**
    - 全部消して、時間を測りながらもう一度書く。10分以内に一度もエラーを出さずに書けるようになるまで繰り返す。3回連続成功したら3段階目クリア
    - なぜ10分×3回か: 書く過程で理解が整理され思考が深まる。何度も同じ箇所で間違うなら、その箇所に不自然さがある可能性が高い。長くなりがちな問題は15分程度まで緩めてもよい
4. **レビュー依頼**
    - 3段階目まで終わったら GitHub にあげ、`#レビュー依頼` チャンネルで同じ問題を解いた人を5人ほどメンションする
    - GitHub が難しいうちは、Discord の自分のチャンネルに ```python ``` のコードブロックで投稿するだけでもよい
5. **レビューを踏まえて書き直す**
    - もらったコメントを反映し、必要なら再度10分チャレンジをやり直す

### 書く前・書いた後に確認すること

- 実装前に時間計算量を見積もる
    - 計算量の式に制約の最大サイズを代入しておおよそのステップ数を出し、言語ごとの1秒あたり処理可能ステップ数（Python: 約100万〜1000万steps/秒）で割って実行時間を概算してから実装する
- 提出に頼らず自分で正誤を検証する
    - Submit で正誤がわかるからといって確認を省略せず、提出前に自分でロジックを検証する

### 進行中のコミュニケーション

- 次に解く問題を事前に予告する（前の問題のレビューを依頼するタイミングで）
- 手を付け始めた瞬間にその旨を書き込む
- 15分考えて分からなければ、そこまで考えたことを言語化して共有する
- 動かないコードができて直せなければ、状況をそのまま投げる
- 困ったときは積極的に助けを求める。応答がなくなるよりも、細かく刻んで投稿する方がよい

### 慣れてきたら

- 他人のコードにコメントしてフィードバックする
- 自分の解法と他人の解法で考え方にどう違いがあるか、違いの良し悪しを考える
- 他人へのコメントから連想される知識を書き出して調べる
- 入力に想定外の値が来たときの挙動を考えておく
- 使っている標準ライブラリのドキュメントを読む。知らないオプションがあり、使った方がよい場合がある
- 自分の実装と似た機能が標準ライブラリにあれば、そのソースコードを読む（Python なら CPython）

### 関連する取り組み

- LeetCode の解法で使われているライブラリ（`@lru_cache`、`heapq` など）を自分で再実装してみる
- CPython のソースコードを読む

### 心構え

- コードがアクセプトされること自体は大したことではない。専門家が自然に感じる反応や感覚（ドキュメントを見たくなる、など）を身につけることが目標
- この練習は仕事の引き継ぎだと捉える。最終的には自分がレビューをする側、練習会を開く側になれることを目指す
- 感情や審美眼を養う。「これが絶対で他は許せない」ではなく、「個人的にはこれが好み」という程度の幅を持てるとよい

## 実装を読みたい関数・ライブラリ一覧

これまでの解答や調査で使った（または検討した）標準ライブラリの関数・メソッド。「慣れてきたら」の実装読解の対象リストとして使う。

### コレクション・探索系
- [ ] `collections.deque`（`append` / `popleft` / `pop`）— 104（検討）, 111（採用）, 200（検討）
- [ ] `set`（`add` / `in`）— 104（初期案）, 141, 200
- [ ] `dict` / `enumerate`— 1, 20
- [x] `_collections` モジュールの在り処（`collections.__file__`で特定済み）— 20（ファイル位置のみ確認、中身は未読）

### キュー系
- [ ] `queue.Queue`— 111, 200（検討したが未採用）
- [ ] `queue.LifoQueue`— 20（検討したが未採用）

### ヒープ系
- [x] `heapq.heappush` / `heapq.heappushpop`— 703（採用、使い方は理解済み。CPython実装は未読）
- [ ] `heapq.heapify`— 200, 703（検討）
- [ ] `heapq.heappop`— 200（検討）
- [ ] `heapq._siftup`（`heapify`内部）— 703（CPython実装を読み始めたが途中で断念、再挑戦したい）

### ソート系
- [ ] `sorted()`— 1, 703（検討したが未採用）

### その他
- [ ] `dataclasses.dataclass`— 111（他の人のコードで遭遇、使い方のみ確認）
- [ ] `sys.getrecursionlimit` / `sys.setrecursionlimit`— 104
- [ ] `sys.maxsize`— 111
- [ ] `sys.getsizeof`— 111
- [ ] `time.perf_counter`— 1

## 参考資料

- [コーディング練習会参加マニュアル](https://docs.google.com/document/d/1bjbOSs-Ac0G_cjVzJ2Qd8URoU_0BNirZ8utS3CUAeLE/edit?tab=t.0#heading=h.y1cq1o8g4nbl)
- [コーディング練習会典型コメント集](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.gp4hkfr3qfqc)

## 進捗

出典: [LeetCode problem list](https://leetcode.com/list/xo2bgr0r)

### LinkedList
- [x] Linked List Cycle (Easy)
- [ ] Linked List Cycle II (Medium)
- [ ] Remove Duplicates from Sorted List (Easy)
- [ ] Remove Duplicates from Sorted List II (Medium)
- [ ] Add Two Numbers (Medium)

### Stack
- [x] Valid Parentheses (Easy)
- [ ] Reverse Linked List (Easy)

### Heap, PriorityQueue
- [x] Kth Largest Element in a Stream (Easy)
- [ ] Top K Frequent Elements (Medium)
- [ ] Find K Pairs with Smallest Sums (Medium)

### HashMap
- [x] Two Sum (Easy)
- [ ] Group Anagrams (Medium)
- [ ] Intersection of Two Arrays (Easy)
- [ ] Unique Email Addresses (Easy)
- [ ] First Unique Character in a String (Easy)
- [ ] Subarray Sum Equals K (Medium)

### Graph, BFS, DFS
- [x] Number of Islands (Medium)
- [ ] Max Area of Island (Medium)
- [ ] Number of Connected Components in an Undirected Graph (Medium)
- [ ] Word Ladder (Medium)

### Tree, BST
- [x] Maximum Depth of Binary Tree (Easy)
- [x] Minimum Depth of Binary Tree (Easy)
- [ ] Merge Two Binary Trees (Easy)
- [ ] Convert Sorted Array to Binary Search Tree (Easy)
- [ ] Path Sum (Easy)
- [ ] Binary Tree Level Order Traversal (Medium)
- [ ] Binary Tree Zigzag Level Order Traversal (Medium)
- [ ] Validate Binary Search Tree (Medium)
- [ ] Construct Binary Tree from Preorder and Inorder Traversal (Medium)

### Dynamic Programming
- [ ] ~~Paint Fence (Easy)~~ (無料枠では解けないため対象外)
- [ ] Longest Increasing Subsequence (Medium)
- [ ] Maximum Subarray (Easy)
- [ ] Unique Paths (Medium)
- [ ] Unique Paths II (Medium)
- [ ] House Robber (Easy)
- [ ] House Robber II (Medium)
- [ ] Best Time to Buy and Sell Stock (Easy)
- [ ] Best Time to Buy and Sell Stock II (Easy)
- [ ] Word Break (Medium)
- [ ] Coin Change (Medium)

### Binary Search
- [ ] Search Insert Position (Easy)
- [ ] Find Minimum in Rotated Sorted Array (Medium)
- [ ] Search in Rotated Sorted Array (Medium)
- [ ] Capacity To Ship Packages Within D Days (Medium)

### Recursion
- [ ] Pow(x, n) (Medium)
- [ ] K-th Symbol in Grammar (Medium)
- [ ] Split BST (Medium)

### Sliding Window
- [ ] Longest Substring Without Repeating Characters (Medium)
- [ ] Minimum Size Subarray Sum (Medium)

### Greedy + Backtracking
- [ ] Permutations (Medium)
- [ ] Subsets (Medium)
- [ ] Combination Sum (Medium)
- [ ] Generate Parentheses (Medium)

### Others
- [ ] Move Zeroes (Easy)
- [ ] Meeting Rooms (Easy)
- [ ] Meeting Rooms II (Medium)
- [ ] Is Subsequence (Medium)
- [ ] Next Permutation (Medium)
- [ ] String to Integer (atoi) (Medium)
- [ ] ZigZag Conversion (Medium)