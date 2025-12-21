# ==========================================
# SCENARIO:
# Write a function to validate if a configuration string has balanced brackets.
# This mimics checking syntax for JSON, code blocks, or nested configs.
# Examples:
# "{[]}" -> True
# "{[}]" -> False (Mismatched nesting)
# "((("  -> False (Unclosed)
# ==========================================

def is_balanced(s):
    print(f"Checking: '{s}'")
    
    # Stack data structure: Last-In, First-Out (LIFO)
    stack = []
    
    # Map closing brackets to their corresponding opening brackets
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping.values():
            # If it's an opening bracket, push to stack
            stack.append(char)
        elif char in mapping:
            # If it's a closing bracket...
            
            # 1. Check if stack is empty (matches nothing)
            if not stack:
                return False
            
            # 2. Pop the top element
            top_element = stack.pop()
            
            # 3. Check if it matches the current closing bracket
            if mapping[char] != top_element:
                return False
        else:
            # Ignore non-bracket characters (optional, depending on requirements)
            continue
            
    # If stack is empty, all brackets were closed correctly
    return len(stack) == 0

# ==========================================
# SCENARIO 2: FizzBuzz Variant (Classic Check)
# "Print numbers 1 to n.
#  If divisible by 3, print 'Dev'.
#  If divisible by 5, print 'Ops'.
#  If divisible by both, print 'DevOps'."
# ==========================================
def devops_fizzbuzz(n=15):
    print(f"\n--- DevOps FizzBuzz (n={n}) ---")
    results = []
    for i in range(1, n + 1):
        output = ""
        if i % 3 == 0:
            output += "Dev"
        if i % 5 == 0:
            output += "Ops"
        
        # If output is empty, just use the number
        results.append(output or str(i))
        
    print(", ".join(results))

if __name__ == "__main__":
    # Test Cases for Balanced Brackets
    print(f"Result: {is_balanced('{[]}')}\n")   # True
    print(f"Result: {is_balanced('{[}]')}\n")   # False
    print(f"Result: {is_balanced('(((')}\n")    # False
    
    devops_fizzbuzz()
