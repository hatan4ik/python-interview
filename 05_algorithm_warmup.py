from typing import List, Dict

# ==========================================
# SCENARIO:
# Algorithms with Type Hints.
# ==========================================

def is_balanced(s: str) -> bool:
    print(f"Checking: '{s}'")
    
    stack: List[str] = []
    
    # Mapping closing -> opening
    mapping: Dict[str, str] = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            # Walrus operator to check empty stack AND pop in safe way? 
            # (Standard logic is actually cleaner here, keeping it simple)
            if not stack:
                return False
            
            top_element = stack.pop()
            
            if mapping[char] != top_element:
                return False
        else:
            continue
            
    return len(stack) == 0

def devops_fizzbuzz(n: int = 15) -> None:
    print(f"\n--- DevOps FizzBuzz (n={n}) ---")
    results: List[str] = []
    
    for i in range(1, n + 1):
        output = ""
        if i % 3 == 0:
            output += "Dev"
        if i % 5 == 0:
            output += "Ops"
        
        # 'or' short-circuit optimization
        results.append(output or str(i))
        
    print(", ".join(results))

if __name__ == "__main__":
    print(f"Result: {is_balanced('{[]}')}\n")   # True
    print(f"Result: {is_balanced('{[}]')}\n")   # False
    print(f"Result: {is_balanced('(((')}\n")    # False
    
    devops_fizzbuzz()