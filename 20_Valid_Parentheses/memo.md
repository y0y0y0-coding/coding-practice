## 問題
- https://leetcode.com/problems/valid-parentheses/

## メモ（感想や調べたことなど）
### Step1
- 問題のカテゴリがStackだったので、Stackを使うと予想してしまう
    - この発想で取り組むのは良くない。。
- 文字を先頭からチェックし、
    - Stackの末尾がopen bracket、チェックする文字が対応するclose bracket
        - 末尾のopen bracketをpop
    - Stackの末尾がopen bracket、チェックする文字が対応しないopen bracket
        - close bracketをstackにいれる
    - Stackの末尾がopen bracket、チェックする文字がclose bracket
        - false
- と書いていったら、Stackにclose bracketを挿入しないことに気がつく
- ここでちょっと手が止まる。。条件分岐をどのようにするか。

```
for check_letter in s:
    # チェックする文字がopen bracketならstackに挿入
    if xxxxx

    # 以降、チェックする文字はclose bracketになる
    ## stackが空なら終了
    if xxxxxx
        return False

    ## stackの末尾が対応するopen bracketなら、stackの末尾をpop
    if xxxxx
    if xxxxx
    if xxxxx

    ## close bracketをstackに挿入できないので終了
    return False

# 判定
## stackが空ならTrue
## stackに値が入っていたらFalse
```

- 開始して、25分も経っていた。。
- 書いてみる。

- stackの変数名で良いものが思いつかなかった。

```
        check_stack = []
        for check_letter in s:
            if check_stack == "(" or check_letter == "[" or check_letter == "{":
                check_stack.append(s)
            
            if check_stack == []:
                return False

            if check_stack[-1] == "(" and check_letter == ")":
                check_stack.pop()
            if check_stack[-1] == "[" and check_letter == "]":
                check_stack.pop()
            if check_stack[-1] == "{" and check_letter == "}":
                check_stack.pop()

            return False

        if check_stack == []:
            return True
        else:
            return False
```

- そしてテストに通らない
- check_stackとcheck_letterを取り街がている箇所がある
    - 先頭がcheckで被っていると可読性が低そう
-check_stack → bracket_stackに変更する

```
class Solution:
    def isValid(self, s: str) -> bool:

        bracket_stack = []
        for check_letter in s:
            if check_letter == "(" or check_letter == "[" or check_letter == "{":
                bracket_stack.append(s)
            
            if bracket_stack == []:
                return False

            if bracket_stack[-1] == "(" and check_letter == ")":
                bracket_stack.pop()
            if bracket_stack[-1] == "[" and check_letter == "]":
                bracket_stack.pop()
            if bracket_stack[-1] == "{" and check_letter == "}":
                bracket_stack.pop()

            return False

        if bracket_stack == []:
            return True
        else:
            return False
```

- 通らないのでローカルでテスト

```
class Solution:
    def isValid(self, s: str) -> bool:

        bracket_stack = []
        for check_letter in s:
            if check_letter == "(" or check_letter == "[" or check_letter == "{":
                bracket_stack.append(s)
            
            if bracket_stack == []:
                return False

            if bracket_stack[-1] == "(" and check_letter == ")":
                bracket_stack.pop()
            if bracket_stack[-1] == "[" and check_letter == "]":
                bracket_stack.pop()
            if bracket_stack[-1] == "{" and check_letter == "}":
                bracket_stack.pop()

            return False

        if bracket_stack == []:
            return True
        else:
            return False

# ローカルテスト
if __name__ == "__main__":
    sol = Solution()
    print(sol.isValid("()"))      # 期待値 True
    print(sol.isValid("()[]{}"))  # 期待値 True
    print(sol.isValid("(]"))      # 期待値 False
```

- 実行結果

```
$ python3 main.py
False
False
False
```

- ここでprintデバックをして、bracket_stackの初期値が空であるため、最初のループでFalseになることに気がついた。

```
            if bracket_stack == []:
                return False
```

- 以下のコード終了後にループから抜け出せていない

```
            if check_letter == "(" or check_letter == "[" or check_letter == "{":
                bracket_stack.append(s)
                continue
``` 

- 流石に時間がかかりすぎているので、答えをみる
- 5分手が止まったら答えをみるルールだけだと、試行錯誤を続けてしまうのでトータル時間がしきい値を超えたら答えをみるルールを追加したほうが良さそう。
- 回答

#### 回答一人目
- https://github.com/Yuto729/leetcode/pull/12/changes
- 読んだ感想
    - 自分の書いたものと比べて、シンプルにまとまっている
    - `open_to_close`というdictでまとめる発想がなかった。
        - 発想がなかったというより、おそらくしていない。
        - 自分のなかで最初に思いついたもので突き進もうとしているかも。
    - stackにopen brancketを挿入する
        - ここは自分の考えと同じ
    - stackが空の場合は、Falseを返す
        - ここも自分の考えと同じ
    - `open_to_close[open_branckets.pop()] != char`
        - stackの末尾とチェックする文字の比較をしている。
            - 自分の考えとの差は、一致していなかったらFalseとまとめている点
            - 自分がかいたものよりかなりシンプルにまとまっているが、方向性はズレていない

```
class Solution:
        def isValid(self, s: str) -> bool:
            open_branckets = []
            open_to_close = {
                '(': ')',
                '{': '}',
                '[': ']'
            }

            for char in s:
                if char in open_to_close:
                    open_branckets.append(char)
                    continue

                if not open_branckets or open_to_close[open_branckets.pop()] != char:
                    return False

            return len(open_branckets) == 0
```

- ここでprintデバックし、自分の回答を見直し

```
$ python3 main.py
['()']
False
['()[]{}']
False
['(]']
False
```

- stackへの追加で、文字列`s`を丸ごと挿入していた。
- `bracket_stack.append(s)` → `bracket_stack.append(check_letter)` に修正

```
            if check_letter == "(" or check_letter == "[" or check_letter == "{":
                bracket_stack.append(s)
```

- テスト通った

```
class Solution:
    def isValid(self, s: str) -> bool:

        bracket_stack = []
        for check_letter in s:
            if check_letter == "(" or check_letter == "[" or check_letter == "{":
                bracket_stack.append(check_letter)
                continue
            
            if bracket_stack == []:
                return False

            if bracket_stack[-1] == "(" and check_letter == ")":
                bracket_stack.pop()
                continue
            if bracket_stack[-1] == "[" and check_letter == "]":
                bracket_stack.pop()
                continue
            if bracket_stack[-1] == "{" and check_letter == "}":
                bracket_stack.pop()
                continue

            return False

        if bracket_stack == []:
            return True
        else:
            return False

# ローカルテスト
if __name__ == "__main__":
    sol = Solution()
    print(sol.isValid("()"))      # 期待値 True
    print(sol.isValid("()[]{}"))  # 期待値 True
    print(sol.isValid("(]"))      # 期待値 False
```

- コードを整える。
- 確認した回答はbracketのペアを辞書でまとめていた

```
            open_to_close = {
                '(': ')',
                '{': '}',
                '[': ']'
            }
```

- 私の書き方ではbracketが新たに増えるとif文、if文の条件文を書き足す必要がある。
    - 私も辞書でまとめることにした。
    - 変数名は模範解答より、よりものが思いつかないため、そのまま使う
- 次にstackの変数名について。
    - open bracketのみ挿入するため、openという文字をいれたい。しかし、stackの使い方をすることを明示するため、stackという文字もいれる
    - `open_bracket_stack` にする
- チェックする文字`check_letter`とあるが、この問題はbracketしかないため、`check_bracket`にする
- 対応するbracketを辞書でまとめたので、forループのif文処理を書き直し
- もとのコードでは最後に`return False`を書いたが、処理内容をコメントに書いていくうちに、`else return`のほうが自然と感じたため、変更した

```
            # check_bracketとstack末尾のopen bracketに対応するclose bracketの組み合わせをチェック
            # 組み合わせが対応して場合、stack末尾の値をpop
            if check_bracket == open_to_close[open_bracket_stack[-1]]:
                open_bracket_stack.pop()
                continue
            # 組み合わせが対応してない場合、終了
            else:
                return False
```

- 参考にしたコードでは、stackが空の場合の処理とstack末尾のチェックをまとめて書いていた。
- なやましいが、私の思考の流れのように書くことを優先した。

```
                if not open_branckets or open_to_close[open_branckets.pop()] != char:
                    return False
```

- いったん以下のコードを10分以内にかけるか確認

```
class Solution:
    def isValid(self, s: str) -> bool:

        open_bracket_stack = []
        open_to_close = {
            '(' : ')',
            '{' : '}',
            '[' : ']'
        }

        for check_bracket in s:

            # check_bracketがopen bracketの場合、stackに挿入
            if check_bracket in open_to_close:
                open_bracket_stack.append(check_bracket)
                continue

            # 最初のif文でcheck_bracketがopen bracketの場合の処理をしている
            # そのため、これ以降の処理ではcheck_bracketはclose bracketとなる

            # stackが空の場合、close bracketを挿入できない
            if open_bracket_stack == []:
                return False

            # check_bracketとstack末尾のopen bracketに対応するclose bracketの組み合わせをチェック
            # 組み合わせが対応して場合、stack末尾の値をpop
            if check_bracket == open_to_close[open_bracket_stack[-1]]:
                open_bracket_stack.pop()
                continue
            # 組み合わせが対応してない場合、終了
            else:
                return False

        if open_bracket_stack == []:
            return True
        else:
            return False
```

### Step2
- 3回連続で10分以内に書けるかを確認。
- 3回連続で10分以内に書けたのでpushする。
    - やってみたら5分程度で書けているので驚いた。
- [コメント集](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.ns0bie22a6m) を読む
- `個人的には1問1時間位で考えています。あまり長いと退屈に感じるでしょう`
        - やはり時間を書けすぎているので、初回は全体の制限時間を決めてみる

```
> Built-in Exceptions を一通り見ておきましょう。
> この文脈で、一番近い Exception はどれかも考えてみましょう。
> ここに3つ大事なことがあります。
> 1. 「公式ドキュメントに目を通す」という行動を取りたくなること自体が大事です。つまり、結果ではなくて欲求を評価しましょう。
> 2. 何を使うかではなくて、何は不適切であると感じたかも大事です。つまり、結果ではなくて過程を評価しましょう。
> 3. 最終的にはエンジニアリングという目的との関係から評価します。つまり、結果ではなくて目的を評価しましょう。
> これは、練習すべてに通じることかと思います。
```

- まだ、コードを書くことを優先して公式ドキュメントを読みたい気持ちになっていない。

