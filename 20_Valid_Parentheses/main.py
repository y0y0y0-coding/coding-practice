class Solution:
    def isValid(self, s:str) -> bool:
        open_brackets = []
        open_to_close = {
            '(' : ')',
            '{' : '}',
            '[' : ']'
        }

        for check_bracket in s:
            if check_bracket in open_to_close:
                open_brackets.append(check_bracket)
                continue

            if len(open_brackets) == 0:
                return False

            if check_bracket == open_to_close[open_brackets[-1]]:
                open_brackets.pop()
                continue

            return False

        if len(check_bracket) == 0:
            return True
        else:
            return False

# ローカルテスト
if __name__ == "__main__":
    sol = Solution()
    #print(sol.isValid("()"))      # 期待値 True
    #print(sol.isValid("()[]{}"))  # 期待値 True
    #print(sol.isValid("(]"))      # 期待値 False
    print(sol.isValid("(])"))      # 期待値 False