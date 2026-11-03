class Soution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        max_lengths = [1] * len(nums)

        for idx in range(len(nums)):
            for pre_idx in range(idx):
                if nums[pre_idx] < nums[idx]:
                    max_lengths[idx] = max(max_lengths[pre_idx] + 1, max_lengths[idx])

        return max(max_lengths)
