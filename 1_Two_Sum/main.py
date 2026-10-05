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