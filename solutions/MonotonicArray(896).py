"""
Topic: Arrays
Difficulty: Easy

Question: 896. Monotonic Array

An array is monotonic if it is either monotone increasing or monotone decreasing.

An array nums is monotone increasing if for all i <= j, nums[i] <= nums[j]. 
An array nums is monotone decreasing if for all i <= j, nums[i] >= nums[j].

Given an integer array nums, return true if the given array is monotonic, or false otherwise.

Path: solutions/MonoTonicArray(896).py  

"""

from typing import List

class Solution:
    def isMonotonic(self, nums: List[int]) -> bool:
        num1 = list(nums)
        num1.sort()
        if nums == num1 or nums == num1[::-1]:
            return True
        return False
        