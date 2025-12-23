# How to Read Problems & Write Pseudocode Like a Pro
*The Meta-Skill of Passing Technical Interviews*

This guide isn't about *what* code to write, but *how to think* and *how to communicate* your solution before you type a single line of Python.

---

## Part 1: The "3-Pass Read" Technique
Most candidates fail because they start coding immediately. **Pros start by reading.**

### Pass 1: The "High Level" Scan
**Goal:** Understand the story.
*   *Question:* "What is the input? What is the output?"
*   *Action:* Identify the data types.
    *   Input: `List of Strings`? `Integer`? `Stream of data`?
    *   Output: `Boolean`? `Sorted List`? `Integer (Index)`?

### Pass 2: The "Constraint" Hunt
**Goal:** Identify the boundaries.
*   *Question:* "How big is the data? Can it be negative? Can it be empty?"
*   *Action:* Look for keywords:
    *   "Sorted" -> Suggests Binary Search ($O(\log n)$) or Two Pointers.
    *   "Continuous" -> Suggests Sliding Window.
    *   "Shortest/Minimum" -> Suggests BFS or DP.
    *   "Top K" -> Suggests Heap.
    *   "10 GB of data" -> Suggests external sort or processing in chunks (cannot fit in RAM).

### Pass 3: The "Edge Case" Simulation
**Goal:** Break your own logic before you build it.
*   *Action:* Write down 3 test cases immediately:
    1.  **Happy Path:** The standard example given.
    2.  **Empty/Null:** Input is `[]`, `""`, or `None`.
    3.  **Massive/Tiny:** Input is 0, or Input is $10^9$.

---

## Part 2: Writing "PRO" Pseudocode

"Pro" pseudocode is **Language Agnostic** but **Structurally Rigorous**. It should read like English but look like code.

### The Golden Rules
1.  **Capitalize Keywords:** `IF`, `ELSE`, `FOR`, `WHILE`, `RETURN`, `FUNCTION`.
2.  **Indentation Matters:** Use whitespace to show blocks (just like Python).
3.  **Descriptive Variables:** `i` is bad. `current_index` is good.
4.  **No Syntax Sugar:** Don't use `[::2]` (Python specific). Use `increment index by 2`.

### Example: "Move Zeroes"
**Problem:** Move all zeroes in an array to the end while maintaining the order of non-zero elements.

#### ❌ Bad Pseudocode (Too Vague)
```text
loop through the array
if we see a number that isn't zero
put it in the new list
fill the rest with zeros
```
*Why it fails:* It hides the complexity. "Put it in the new list" doesn't say *how* (Do we create a new array? O(N) space? Can we do it in-place?).

#### ⚠️ Junior Pseudocode (Too Pythonic)
```text
def move_zeroes(nums):
    new_list = []
    for x in nums:
        if x != 0:
            new_list.append(x)
    while len(new_list) < len(nums):
        new_list.append(0)
    return new_list
```
*Why it fails:* You just wrote Python code on a whiteboard. If the interviewer wanted C++, this is useless. It also wastes memory (O(N) space).

#### ✅ PRO Pseudocode (Algorithmic & Clear)
```text
FUNCTION move_zeroes(arr):
    # Use 'Two Pointer' approach for O(1) Space
    INITIALIZE 'write_pointer' = 0
    
    # 1. Shift non-zero values forward
    FOR 'read_pointer' FROM 0 TO length(arr) - 1:
        current_val = arr[read_pointer]
        
        IF current_val IS NOT 0:
            arr[write_pointer] = current_val
            INCREMENT 'write_pointer'
            
    # 2. Fill remaining spots with 0
    WHILE 'write_pointer' < length(arr):
        arr[write_pointer] = 0
        INCREMENT 'write_pointer'
        
    RETURN arr
```
*Why this wins:*
*   Explicitly mentions the strategy ("Two Pointer").
*   Clearly separates the two phases (Shift vs Fill).
*   Uses universal logic (`FOR`, `WHILE`, `INCREMENT`) valid in Java, Go, C, or Python.

---

## Part 3: The "Talk-Write" Protocol
During the interview, **Silence is Death**. You must narrate your pseudocode.

**The Script:**
1.  **State Intent:** "I'm going to track two pointers. One to read the array, one to write the valid numbers."
2.  **Write the Line:** (Write `INITIALIZE write_pointer = 0`)
3.  **Justify:** "I need this variable to remember the last position where I placed a non-zero element."

## Part 4: Practice Template
Use this template for every practice problem:

```text
PROBLEM: [Name]

CONSTRAINTS:
- Time: O(N) preferred?
- Space: O(1) required?
- Inputs: [Type, Range]

STRATEGY: [Name of Algo, e.g., Sliding Window]

PSEUDOCODE:
FUNCTION solution(input):
    VALIDATE input (handle edge cases)
    
    INITIALIZE variables
    
    LOOP condition:
        LOGIC step 1
        LOGIC step 2
        
    RETURN result
```
