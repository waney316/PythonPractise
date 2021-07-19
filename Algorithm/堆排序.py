# 堆排序主要采用python内置数据结构headp默认最小堆
import heapq

def Heapsort(array):
    if len(array) < 1:
        return array
    # 将传入的数组构建为堆序列
    heap = []
    array = [-num for num in array]
    for num in array:
        # 默认为最小堆，如果需要从大到小排序传递-值
        heapq.heappush(heap, num)
    # 默认堆为最小堆排序
    res = []
    for _ in range(0, len(array)):
        res.append(-(heapq.heappop(heap)))
    return res

if __name__ == '__main__':
    array = [1,4,3,6,9,2,0,24,15,67,]
    print(Heapsort(array))