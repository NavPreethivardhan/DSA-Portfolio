"""
Topic: Arrays, Two Pointers, Sorting
Difficulty: Easy

Question: 905. Sort Array By Parity

Given an integer array nums, move all the even integers at the beginning of the array followed by all the odd integers.

Return any array that satisfies this condition.

Path: solutions/SortArrayByParity(905).py  

"""

from typing import List

class Solution:
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        odd,even = [],[]
        for i in nums:
            if i % 2 == 0:
                even.append(i)
            else:
                odd.append(i)
        return even+odd


        