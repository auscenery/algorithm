from operator import itemgetter


class RangeModule:
    def __init__(self):
        self.ranges = []

    def addRange(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: void
        """
        if not self.ranges:
            self.ranges.append([left, right])
            return

        # 将[left, right)插入或者合并到self.ranges中，如果直接排序时间复杂度为O(nlogn),
        # 这里考虑非排序方法, 时间复杂度为O(n), 空间复杂度为O(n)，目的就是找到合并的起点和终点
        for i, interval in enumerate(self.ranges):
            start, end = interval
            if left < start:
                if right < start:
                    # 插入操作时间复杂度为O(n)
                    self.ranges.insert(i, [left, right])
                    return
                if right == start:
                    self.ranges[i][0] = left
                    return
                if right > start and right <= end:
                    self.ranges[i][0] = left
                    return
                if right > end:
                    # 考虑下一个，可能有合并
                    self._merge_interval_by_right_value(i, left, right)
                    return
                pass
            elif left == start:
                if right <= end:
                    return
                if right > end:
                    # 考虑下一个， 可能有合并
                    self._merge_interval_by_right_value(i, left, right)
                    return
            else:# left > start
                if left < end:
                    if right <= end:
                        return # 被包含
                    if right > end:
                        # 考虑下一个，可能有合并
                        self._merge_interval_by_right_value(i, left, right)
                        return
                if left == end:
                    # 考虑下一个，可能有合并
                    self._merge_interval_by_right_value(i, left, right)
                    return
                if left > end: # 继续下一轮循环
                    continue

    def _merge_interval_by_right_value(self, start_index, left, right):
        """
            从区间self.ranges[start_index]开始合并,即， 根据type类型来找到合并到哪里为止即可，从而结束
            记start, end = self.ranges[start_index]
            这里的right > end 一直成立
        """
        self.ranges[start_index][0] = min(self.ranges[start_index][0], left)
        # 找到right插入的位置, 并删除中间的节点
        for i in range(start_index + 1, len(self.ranges)):
            if right < self.ranges[i][0]:
                del self.ranges[start_index+1: i]
                self.ranges[start_index][1] = right
                return
            
            if right <= self.ranges[i][1]:
                right = self.ranges[i][1]
                del self.ranges[start_index+1: i+1]
                self.ranges[start_index][1] = right
                return
                

    def queryRange(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: bool
        """
        pos = self._search(left, right)
        return True if pos != -1 else False

    def removeRange(self, left, right):
        """
        split merge
        :type left: int
        :type right: int
        :rtype: void
        S(n) = O(n), T(n) = O(n)
        """
        temp_ranges = []
        for i, interval in enumerate(self.ranges):
            # completely not contains, small, end and exit loop
            if right <= interval[0]:
                temp_ranges.extend(self.ranges[i:])
                break
            # completely not contains, larger
            if left >= interval[1]:
                temp_ranges.append(interval)
                continue

            # partially contains, left part
            if interval[0] <= left and interval[1] <= right:
                if interval[0] < left:
                    temp_ranges.append([interval[0], left])
                continue

            # partially contains, right part, end and exit loop
            if interval[0] >= left and interval[1] >= right:
                if interval[1] > right:
                    temp_ranges.append([right, interval[1]])
                temp_ranges.extend(self.ranges[i + 1:])
                break

            # all contains case1, interval 属于 [left, right)
            if interval[0] >= left and interval[1] <= right:
                continue

            # all contains case2, [left, right) 属于interval
            if interval[0] <= left and interval[1] >= right:
                if interval[0] < left:
                    temp_ranges.append([[interval[0], left]])
                if interval[1] > right:
                    temp_ranges.append([[right, interval[1]]])
                temp_ranges.extend(self.ranges[i+1:])
                break

        self.ranges = temp_ranges

    def _search(self, left, right):
        """return the pos of intervals, return -1 not found"""
        for pos, interval in enumerate(self.ranges):
            start, end = interval
            # continue to next interval
            if left > end:
                continue
            # left and right all not contains
            if right <= start:
                return -1

            # all contians
            if left >= start and right <= end:
                return pos

            # right part not all contains
            if left >= start and right > end:
                return -1

            # left part not all contains
            if left < start and right <= end:
                return -1

        return -1


if __name__ == "__main__":
    rgm = RangeModule()
    print(rgm.ranges)

    rgm.addRange(5, 8)
    print(rgm.ranges)

    print(rgm.queryRange(3, 4))

    rgm.removeRange(5, 6)
    print(rgm.ranges)

    rgm.removeRange(3, 6)
    print(rgm.ranges)

    rgm.addRange(1, 3)
    print(rgm.ranges)

    rgm.queryRange(2, 3)
    print(rgm.ranges)

    rgm.addRange(4, 8)
    print(rgm.ranges)

    print(rgm.queryRange(2, 3))

    rgm.removeRange(4, 9)
    print(rgm.ranges)