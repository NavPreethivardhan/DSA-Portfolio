"""
Template: Dynamic Programming Patterns
Topic: Dynamic Programming
Difficulty: Template
"""

def dp_template(n, transition):
    """
    Generic DP framework.
    n: number of states
    transition(dp, i): computes dp[i] based on dp[0..i-1]
    """
    dp = [0] * n
    for i in range(n):
        dp[i] = transition(dp, i)
    return dp

if __name__ == "__main__":
    # Fibonacci example
    def fib_transition(dp, i):
        if i < 2:
            return i
        return dp[i-1] + dp[i-2]
    print(dp_template(10, fib_transition))  # First 10 Fibonacci numbers
