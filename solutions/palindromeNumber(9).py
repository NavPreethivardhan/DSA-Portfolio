"""
Topic: Math
Difficulty: Easy

Question: Palindrome Number
Given an integer x, return true if x is a palindrome, and false otherwise.
Path: solutions/palindromeNumber(9).py  

"""

class Solution:
    def isPalindrome(self, x: int) -> bool:
        x = str(x)
        return x == x[::-1]

        