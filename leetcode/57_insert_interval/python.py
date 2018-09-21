#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Given a set of non-overlapping intervals, insert a new interval into the intervals (merge if necessary).

You may assume that the intervals were initially sorted according to their start times.

Example 1:

Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]
Example 2:

Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].
"""

import operator

# Definition for an interval.
class Interval(object):
     def __init__(self, s=0, e=0):
         self.start = s
         self.end = e

class Solution(object):
    def insert(self, intervals, newInterval):
        """
        :type intervals: List[Interval]
        :type newInterval: Interval
        :rtype: List[Interval]
        """
        # newInterval is empty
        if not newInterval:
            return intervals
        
        # intervals is empty
        if not intervals:
            return [newInterval]
       
        intervals.append(newInterval)
        intervals.sort(key=operator.attrgetter('start', 'end'))
        results = []
        for item in intervals:
            # this step is important, because size change by merge every time
            size = len(results)
            if size > 0 and results[size-1].end >= item.start:
                results[size - 1].end = max(results[size-1].end, item.end)
            else:
                results.append(item)
        return results
