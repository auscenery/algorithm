#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
A Range Module is a module that tracks aranges of numbers. Your task is to design and implement the following interfaces in an efficient manner.

addRange(int left, int right) Adds the half-open interval [left, right), tracking every real number in that interval. Adding an interval that partially overlaps with currently tracked numbers should add any numbers in the interval [left, right) that are not already tracked.
queryRange(int left, int right) Returns true if and only if every real number in the interval [left, right) is currently being tracked.
removeRange(int left, int right) Stops tracking every real number currently being tracked in the interval [left, right).

Example 1:
addRange(10, 20): null
removeRange(14, 16): null
queryRange(10, 14): true (Every number in [10, 14) is being tracked)
queryRange(13, 15): false (Numbers like 14, 14.03, 14.17 in [13, 15) are not being tracked)
queryRange(16, 17): true (The number 16 in [16, 17) is still being tracked, despite the remove operation)
Note:

A half open interval [left, right) denotes all real numbers left <= x < right.
0 < left < right < 10^9 in all calls to addRange, queryRange, removeRange.
The total number of calls to addRange in a single test case is at most 1000.
The total number of calls to queryRange in a single test case is at most 5000.
The total number of calls to removeRange in a single test case is at most 1000.
"""

from operator import itemgetter

class RangeModule:

    def __init__(self):
        self.aranges = []
        self.rranges = []

    def addRange(self, left, right):
        """
        :type left: int
        :type right: int
        :rtype: void
        """
        self.aranges = self._sortRange(self.aranges, left, right)
        
            
    def queryRange(self, left, right):
        """
        binary search interval
        :type left: int
        :type right: int
        :rtype: bool
        """
        # first to search self.rranges
        pos = self._anySearch(self.rranges, left, right)
        if pos != -1:
            return False
        # if pos == -1, then search sefl.arangs
        pos = self._allSearch(self.aranges, left, right)
        return True if pos != -1 else False

    def removeRange(self, left, right):
        """
        split merge
        :type left: int
        :type right: int
        :rtype: void
        """
        self.rranges = self._sortRange(self.rranges, left, right)
    
    def _sortRange(self, ranges, left, right):
        """add new elements and sort intervals, T(n) = O(nlogn), S(n) = O(n)"""
        ranges.append([left, right])
        ranges.sort(key=itemgetter(0, 1))
        temp_ranges = []
        for item in ranges:
            sz = len(temp_ranges)
            if sz > 0 and temp_ranges[sz-1][1] >= item[0]:
                temp_ranges[sz-1][1] = max(temp_ranges[sz-1][1], item[1])
            else:
                temp_ranges.append(item)
        return temp_ranges

    def _anySearch(self, ranges, left, right):
        for pos, interval in enumerate(ranges):
            start, end = interval
            # contains part element
            if start <= left <= end:
                return pos
            # contains part element
            if start <= right <= end:
                return pos
            pass

        return -1

    def _allSearch(self, ranges, left, right):
        """return the pos of intervals, return -1 not found"""
        for pos, interval in enumerate(ranges):
            start, end = interval
            # continue to next interval
            if left >= end:
                continue
            # all contians
            if left >= start and right <= end:
                return pos
            
            # right part not all contains
            if left >= start and right > end:
                return -1
            
            # left part not all contains
            if left < start and right <= end:
                return -1
            
            # left and right all not contains
            if left < start:
                return -1
            pass

        return -1