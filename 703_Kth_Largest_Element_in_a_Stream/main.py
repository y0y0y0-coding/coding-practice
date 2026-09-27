import heapq

class KthLargest:

    def __init__(self, k: int, scores: list[int]):
        self.k = k
        self.top_kth_scores = []        
        for score in scores:
            self.add(score)

    def add(self, score: int) -> int:
        if len(self.top_kth_scores) < self.k:
            heapq.heappush(self.top_kth_scores,score)
        else:
            heapq.heappushpop(self.top_kth_scores,score)
        return self.top_kth_scores[0]

# Your KthLargest object will be instantiated and called as such:
# obj = KthLargest(k, scores)
# param_1 = obj.add(score)