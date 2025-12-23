#!/usr/bin/env python3
"""
Algorithmic Warmup.

Classic 'Phone Screen' questions.
1. Balanced Brackets (Stack usage).
2. FizzBuzz (Modulo arithmetic).
"""

from typing import List, Dict

def is_balanced(s: str) -> bool:
    """
    Determines if the brackets in a string are balanced.
    
    Example:
        "{}" -> True
        "{[}]" -> False

    Args:
        s (str): Input string containing brackets.

    Returns:
        bool: True if balanced, False otherwise.
    """
    print(f"Checking: '{s}'")
    
    stack: List[str] = []
    mapping: Dict[str, str] = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        # If it's a closing bracket
        if char in mapping:
            # Pop the top element if stack is not empty, else assign dummy value '#'
            top_element = stack.pop() if stack else '#'
            
            # If the mapped opening bracket doesn't match the top element -> Fail
            if mapping[char] != top_element:
                return False
        # If it's an opening bracket (values of the map)
        elif char in mapping.values():
            stack.append(char)
        else:
            # Non-bracket characters are ignored
            continue
            
    return not stack

def devops_fizzbuzz(n: int = 15) -> None:
    """
    Prints numbers 1 to n with replacements:
    - Divisible by 3 -> "Dev"
    - Divisible by 5 -> "Ops"
    - Both -> "DevOps"

    Args:
        n (int): The number to count up to.
    """
    print(f"\n--- DevOps FizzBuzz (n={n}) ---")
    results: List[str] = []
    
    for i in range(1, n + 1):
        output = ""
        if i % 3 == 0:
            output += "Dev"
        if i % 5 == 0:
            output += "Ops"
        
        results.append(output or str(i))
        
    print(", ".join(results))

if __name__ == "__main__":
    print(f"Result: {is_balanced('{[]}')}\n")   # True
    print(f"Result: {is_balanced('{[}]')}\n")   # False
    
    devops_fizzbuzz()
