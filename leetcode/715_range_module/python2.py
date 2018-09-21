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
        self.ranges.append([left, right])
        self._sortAndMergeRange()

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
        S(n) = O(n)
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

    def _sortAndMergeRange(self):
        """O(nlogn)"""
        self.ranges.sort(key=itemgetter(0, 1))
        temp_ranges = []
        for item in self.ranges:
            sz = len(temp_ranges)
            if sz > 0 and temp_ranges[sz - 1][1] >= item[0]:
                temp_ranges[sz - 1][1] = max(temp_ranges[sz - 1][1], item[1])
            else:
                temp_ranges.append(item)
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

    print(rgm.queryRange(2, 3))
    print(rgm.ranges)

    rgm.addRange(4, 8)
    print(rgm.ranges)

    print(rgm.queryRange(2, 3))

    rgm.removeRange(4, 9)
    print(rgm.ranges)