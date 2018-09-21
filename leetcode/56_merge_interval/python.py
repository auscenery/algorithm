#! /usr/bin/env python3
"""
Given a collection of intervals, merge all overlapping intervals.

Example 1:

Input: [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into [1,6].
Example 2:

Input: [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considerred overlapping.
"""

# Definition for an interval.
 class Interval:
     def __init__(self, s=0, e=0):
         self.start = s
         self.end = e

class Solution:
    def merge(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: List[Interval]
        """
        n = len(intervals)
        if n <= 1:
            return intervals
        from operator import attrgetter
        intervals.sort(key=attrgetter('start', 'end'))
        results = []
        for i, item in enumerate(intervals):
            size = len(results)
            if size > 0 and results[size -1].end >= item.start:
                results[size - 1].end = max(results[size - 1].end, item.end)
            else:
                results.append(item)
        return results
