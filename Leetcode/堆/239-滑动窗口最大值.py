import heapq
import collections

# 最大堆
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:

        self.k = k
        self.nums = nums
        """"比如数组 [3,4,1,2,6,7]  k=3 """
        # 将前k个元素的取反值和索引先扔到列表中，q =[-3,-4,-1]
        q = [(-nums, i) for i in range(k)]
        # 生成最小堆 [-4, -3, -1]
        heapq.heapify(q)

        # 此时最小堆得堆顶的元素取反值就是当前滑动窗口的最大值
        res = [-q[0][0]]

        # 从第k个元素开始
        for i in range(k, len(self.nums)):
            # 向堆里存储数据
            heapq.heappush(q, (-nums[i], i))

            # 值在数组 \textit{nums}nums 中的位置出现在滑动窗口左边界的左侧
            while q[0][1] <= i-k:
                heapq.heappop(q)
            res.append(-q[0][0])
        return res

# 双向队列
class Solution2:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        q = collections.deque()
        for i in range(k):
            while q and nums[i] >= nums[q[-1]]:
                q.pop()
            q.append(i)

        ans = [nums[q[0]]]
        for i in range(k, n):
            while q and nums[i] >= nums[q[-1]]:
                q.pop()
            q.append(i)
            while q[0] <= i - k:
                q.popleft()
            ans.append(nums[q[0]])

        return ans






