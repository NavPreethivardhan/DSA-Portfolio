"""
Topic: HashTable, Arrays
Difficulty: Easy

Question: 2215. Find the Difference of Two Arrays

Given two 0-indexed integer arrays nums1 and nums2, return a list answer of size 2 where:

answer[0] is a list of all distinct integers in nums1 which are not present in nums2.
answer[1] is a list of all distinct integers in nums2 which are not present in nums1.
Note that the integers in the lists may be returned in any order.

Path: solutions/signOfProductOfArray(1822).py  

"""

from typing import List

class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        nums1 = set(nums1)
        nums2 = set(nums2)
        final = [[],[]]
        for i in nums1:
            if i not in nums2:
                final[0].append(i)
        for j in nums2:
            if j not in nums1:
                final[1].append(j)
        return final