class Solution:
    def isValid(self, s: str) -> bool:
        open_bracket_stack = []
        open_to_close = {
            '(' : ')',
            '{' : '}',
            '[' : ']'
        }

        for check_bracket in s:
            if check_bracket in open_to_close:
                open_bracket_stack.append(check_bracket)
                continue

            if open_bracket_stack == []:
                return False

            if check_bracket == open_to_close[open_bracket_stack[-1]]:
                open_bracket_stack.pop()
                continue
            else:
                return False

        if open_bracket_stack == []:
            return True
        else:
            return False

# ローカルテスト
if __name__ == "__main__":
    sol = Solution()
    print(sol.isValid("()"))      # 期待値 True
    print(sol.isValid("()[]{}"))  # 期待値 True
    print(sol.isValid("(]"))      # 期待値 False