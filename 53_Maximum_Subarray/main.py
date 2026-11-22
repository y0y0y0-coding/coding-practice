class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]
        current_sum = nums[0]

        for idx in range(1, len(nums)):
            current_sum = max(current_sum + nums[idx], nums[idx])
            max_sum = max(max_sum, current_sum)

        return max_sum
