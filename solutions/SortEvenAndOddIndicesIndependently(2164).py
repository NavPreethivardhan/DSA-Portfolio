"""
Topic: Sorting, Arrays
Difficulty: Easy

Question: 2164. Sort Even and Odd Indices Independently

You are given a 0-indexed integer array nums. Rearrange the values of nums according to the following rules:

Sort the values at odd indices of nums in non-increasing order.
For example, if nums = [4,1,2,3] before this step, it becomes [4,3,2,1] after. The values at odd indices 1 and 3 are sorted in non-increasing order.
Sort the values at even indices of nums in non-decreasing order.
For example, if nums = [4,1,2,3] before this step, it becomes [2,1,4,3] after. The values at even indices 0 and 2 are sorted in non-decreasing order.
Return the array formed after rearranging the values of nums.

Path: solutions/SortEvenAndOddIndicesIndependently(2164).py  

"""
from typing import List

class Solution:
    def sortEvenOdd(self, nums: List[int]) -> List[int]:
        odd, even = [], []
        final = []
        for i in range(len(nums)):
            if i%2 == 0:
                even.append(nums[i])
            else:
                odd.append(nums[i])
        odd.sort(reverse = True)
        even.sort()
        x = min(len(even),len(odd))
        for i in range(x):
            final.append(even[i])
            final.append(odd[i])
        for i in final:
            if i in even:
                even.remove(i)
            elif i in odd:
                odd.remove(i)
        
        final+=even
        final+=odd
        return final

