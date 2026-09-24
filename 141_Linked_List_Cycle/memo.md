## 問題
- https://leetcode.com/problems/linked-list-cycle/description/

## メモ（感想や調べたことなど）
### Step1
- Linked List は昔何かの本で読んだ覚えがあるが、Pythonでの書いたことはない
    - leetcodeの回答欄のコメントで`class ListNode`が定義されている
        - インスタンス変数でノードの値とネクストポインタを表している
- `head: Optional[ListNode]` の文法がわからず調べる
    - 型ヒント(型アノテーション)という書き方
        - 変数名: 型 で、その変数に入る値の型を注釈する
        - `Optional[X]` は「`X` または `None`」を表す
- 全然わからなかったため他の方の回答をみる
    - https://github.com/Yuto729/leetcode/blob/main/linked-list-cycle/main.md

```
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()

        while head is not None:
            if head in visited:
                return True

            visited.add(head)
            head = head.next
        
        return False
```

- 読んだ感想
    - `head.val`を一切利用していない。自分で考えいるときはどう使うのかを考えていた。別に使わなくてもよい。
    - 与えられたLinded Listを先頭から追っていくという発想は最初に出たが、すでに訪れたnodeをどう記録すればいいかわからなかった。確かにsetにそのまま保存すればよい。
    - 変数の付け方がわかりやすい。

```
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast = head
        slow = head

        while fast and fast.next:
            
            fast = fast.next.next
            slow = slow.next

            if fast == slow:
                return True

        return False
```

- フロイドのうさぎとかめと呼ばれる「有名な」アルゴリズム
    - 常識には入っていない
- `while` 条件の`fast and fast.next` が初見では読み解けなかった
    - `fast` だけでは不十分
    - ループ内で`fast.next.next`にアクセスしているため、`fast.next`が`None`だとエラーになる


### 二段階目
- 10分以内にエラーを出さずに書く
- 1回目
    - 先ほどのコードとは`while`の条件の書き方異なっていた
        - `while head is not None`
        - 読みさすさとしては、もとのコードのほうが良いと判断
    - 「`set()`を使う」と丸暗記してしまっているかも
        - 値の重複を許さないため、リストより`set()`が妥当
    - 検索速度の観点からも`set()`が良い
        - リストは先頭から順に探すので要素数に比例して遅くなる
        - 集合はハッシュを使うので要素数に関係なくほぼ一定

```
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()

        while head:
            if head in visited:
                return True

            visited.add(head)

            head = head.next

        return False
```

- 2回目
    - 以下のような`visited.add(head)`を書かずにテストを実行し、書き飛ばしていたことに気がつく 

```
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()

        while head is not None:
            if head in visited:
                return True

            head = head.next

        return False
```

- 3回目
    - 10分以内に書けた
    - 3回連続で再現できた

```
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()

        while head is not None:
            if head in visited:
                return True

            visited.add(head)
            head = head.next

        return False
```

- 他の人のコードを読む
    - `node = head` と`head`を直接操作していない
- この関数が外部から呼び出されたときの挙動が気になったので調べる
    - Pythonでは関数内で引数の変数に別の値を代入しても、呼び出し側の変数には影響しない
- `set()`の検索速度が早い理由を調べる
- `set()`の公式ドキュメントを読む
    - https://docs.python.org/ja/3/builtins/stdtypes.html#set
    - 集合の要素は ハッシュ可能 なものでなくてはならない
        - ハッシュ可能(hashable)
            - ハッシュ可能なオブジェクトは辞書のキーや集合のメンバーとして使えます。辞書や集合のデータ構造は内部でハッシュ値を使っているからです。
            - Python のイミュータブルな組み込みオブジェクトは、ほとんどがハッシュ可能です。(リストや辞書のような) ミュータブルなコンテナはハッシュ不可能です。
- `set()`の実装を読む
    - PythonのC実装(CPython)
        - https://github.com/python/cpython
    - https://github.com/python/cpython/blob/main/Objects/setobject.c
    - 3000行以上あるコードを読むのは人生で初めてで、正直どのように読んでいけばいいのかわからない。
- `set()`の実装コードを読み解くことに苦戦したため、コードの見直し優先する
- コメントをいただいたので、改めて書いてみる

```
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()

        node = head
        while node is not None:
            if node in visited:
                return True

            visited.add(node)
            node = node.next

        return False
```

- 10分以内に一回もエラーを出さずに書けた
- レビューを依頼する