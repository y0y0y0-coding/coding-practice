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