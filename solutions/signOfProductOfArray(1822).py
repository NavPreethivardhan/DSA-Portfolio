"""
Topic: Math, Arrays
Difficulty: Easy

Question: 1822. Sign of the Product of an Array
Given an array of integers nums, return 1 if the product is positive, -1 if the product is negative, or 0 if the product is zero. 

Implement a function signFunc(x) that returns:

1 if x is positive.
-1 if x is negative.
0 if x is equal to 0.
You are given an integer array nums. Let product be the product of all values in the array nums.

Return signFunc(product)

Path: solutions/signOfProductOfArray(1822).py  

"""

from typing import List

class Solution:
    def arraySign(self, nums: List[int]) -> int:
        total = 1
        for i in nums:
            total *= i
        return signFunc(total)

def signFunc(num:int):
    if num < 0:
        return -1
    elif num >0 :
        return 1
    else:
        return 0
        