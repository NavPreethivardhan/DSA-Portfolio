"""
Topic: Arrays
Difficulty: Easy

Question: 2057. Smallest Index With Equal Value

Given a 0-indexed integer array nums, return the smallest index i of nums such that i mod 10 == nums[i], 
or -1 if such index does not exist.

x mod y denotes the remainder when x is divided by y.

 
Example 1:
Input: nums = [0,2,1,3]
Output: 0
Explanation: nums[0] == 0. The smallest equal index is 0.
Example 2:
Input: nums = [1,2,3]
Output: -1

Path: solutions/SmallestIndexWithEqualValue(2057).py  

"""

from typing import List

class Solution:
    def smallestEqual(self, nums: List[int]) -> int:
        x = range(len(nums))
        for i in x:
            if i % 10 == nums[i]:
                return i
        else:
            return -1

        