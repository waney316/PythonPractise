import heapq

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        # 维护一个存放最大值的数组
        self.nums = nums
        self.k = k
        # 将数组转变为堆
        heapq.heapify(self.nums)

    # 使用最小堆O(logn)
    def add(self, val: int) -> int:
        # 每次进入一个值，向堆里添加,默认添加在堆顶
        heapq.heappush(self.nums, val)

        # 遍历最小堆,当遍历到k值时，即为当前第k大原色
        while len(self.nums) > self.k:
            heapq.heappop(self.nums)
        # 返回数组的第一个值
        return self.nums[0]


    # 使用sort方法：O(n)
    # def add(self, val: int) -> int:
    #     self.nums.append(val)
    #     self.nums.sort(reverse=True)
    #     return self.nums[self.k-1]



kthLargest = KthLargest(1, [4, 5, 8, 2])
print(kthLargest.add(3))
print(kthLargest.add(5))
print(kthLargest.add(10))

