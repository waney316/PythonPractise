class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        # 从头部和尾部分别开始遍历
        beg = 0
        end = len(s) - 1
        # 如果头部和尾部指针相遇，从表示已经走完
        while beg < end:
            s[beg], s[end] = s[end], s[beg]
            # 指针移动
            beg = beg + 1
            end = end - 1