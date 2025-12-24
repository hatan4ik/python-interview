# Python Interview: Pseudocode & Algorithms Guide

This guide covers common interview patterns, providing **Pseudocode**, **Pythonic Logic**, and **Discussion** for each.

---

## 1. Reconstruct Sentence (Index-Word Sorting)

**Problem:**  
You are given two lists of strings. Each string is in the format `"<index>: <word>"`.  
The lists are messy (whitespace). You need to combine them, parse the index and word, and print the sentence sorted by index.

### Pseudocode
```text
FUNCTION reconstruct_sentence(list1, list2):
    COMBINE list1 and list2 into one list 'raw_data'
    INITIALIZE empty list 'parsed_pairs'

    FOR EACH 'item' IN 'raw_data':
        IF 'item' contains ":":
            SPLIT 'item' by ":" into 'index_str' and 'word_str'
            
            STRIP whitespace from 'index_str' and CONVERT to Integer 'index'
            STRIP whitespace from 'word_str' to get clean 'word'
            
            APPEND tuple (index, word) to 'parsed_pairs'
    
    SORT 'parsed_pairs' based on the first element (the index)
    
    EXTRACT only the 'word' from each pair in the sorted list
    JOIN the words with a space separator
    APPEND a period "." at the end
    
    RETURN the final string
```

### Discussion & Tips
*   **The Trap:** The input string `" 2 : quick "` has spaces *everywhere*. A simple `split(':')` leaves you with `" 2 "` and `" quick "`.
*   **The Fix:** Always use `.strip()` immediately after splitting.
*   **Sorting:** In Python, `list.sort(key=lambda x: x[0])` is the standard way to sort by a specific property.
*   **Edge Cases:** What if the index isn't a number? Wrap the conversion in a `try/except` block to handle bad data gracefully.

---

## 2. Credit Card Processing (Luhn Check + Multi-Key Sort)

**Problem:**  
Process a batch of raw credit card strings (e.g., `" 4111-2222... "`).  
1. Clean the strings (remove `-` and spaces).
2. Validate using the **Luhn Algorithm**.
3. Identify Issuer (Visa, Mastercard, Amex).
4. Sort valid cards by **Issuer (Ascending)**, then by **Last 4 Digits (Descending)**.

### Pseudocode
```text
FUNCTION luhn_check(number_string):
    CONVERT number_string to list of integers 'digits'
    REVERSE 'digits'
    INITIALIZE 'checksum' = 0
    
    FOR index, digit IN 'digits':
        IF index is ODD (every second digit):
            doubled_val = digit * 2
            IF doubled_val > 9:
                doubled_val = doubled_val - 9
            ADD doubled_val to 'checksum'
        ELSE:
            ADD digit to 'checksum'
            
    RETURN (checksum MOD 10 equals 0)

FUNCTION process_batch(raw_cards):
    INITIALIZE 'valid_cards' list
    
    FOR EACH 'raw' IN 'raw_cards':
        CLEAN 'raw' (remove spaces, dashes)
        IF 'clean_num' is not numeric: CONTINUE
        
        IF luhn_check(clean_num) IS TRUE:
            DETERMINE 'issuer' (e.g., starts with '4' -> Visa)
            STORE record {issuer, last_4, full_num} in 'valid_cards'
            
    # Sorting with two keys:
    # 1. Issuer (Asc)
    # 2. Last 4 (Desc)
    SORT 'valid_cards' using KEY: (card.issuer, -1 * card.last_4_integer)
    
    RETURN 'valid_cards'
```

### Discussion & Tips
*   **Luhn Algo:** The "double every second digit" rule is standard. If the result > 9, subtracting 9 is mathematically the same as summing the digits (e.g., $18 \rightarrow 1+8=9$, $18-9=9$).
*   **Multi-Key Sorting:** This is a huge interview plus.
    *   Python: `sort(key=lambda x: (x['issuer'], -int(x['last_4'])))
    *   The negative sign on the integer allows you to sort **Descending** while the string (Issuer) sorts **Ascending** in the same pass.

---

## 3. Reorder Log Files (Custom Sorting Rules)

**Problem:**  
Sort a list of logs. Format: `"id content..."`.
*   **Letter-logs:** Content is letters. Sort by content (lexicographically), then by ID.
*   **Digit-logs:** Content is numbers. Maintain original relative order (do not sort).
*   Put all Letter-logs *before* Digit-logs.

### Pseudocode
```text
FUNCTION reorder_logs(logs):
    INITIALIZE 'letter_logs' list
    INITIALIZE 'digit_logs' list
    
    FOR EACH 'log' IN 'logs':
        SPLIT 'log' into 'identifier' and 'content' (max 1 split)
        
        IF first character of 'content' is DIGIT:
            APPEND 'log' to 'digit_logs'
        ELSE:
            # Store tuple for sorting: (content, identifier, full_log_string)
            APPEND (content, identifier, log) to 'letter_logs'
            
    # Sort letter logs
    SORT 'letter_logs' by 'content', then 'identifier'
    
    # Extract original strings
    reconstructed_letters = [log[2] for log in 'letter_logs']
    
    RETURN reconstructed_letters + digit_logs
```

### Discussion & Tips
*   **Stability:** Python's sort is "stable". This implies that if two items compare equal, their original order is preserved. This is vital for the "Digit-logs" requirement.
*   **Tuple Sorting:** Python compares tuples element-by-element. `(a, b) < (c, d)` checks `a < c` first. If they are equal, it checks `b < d`. This perfectly matches the "sort by content, then by ID" rule.

---

## 4. Version Number Comparator (String Parsing Logic)

**Problem:**  
Compare two version strings like `"1.0.1"` and `"1.0"`.  
Rules: `"1.0.1" > "1.0"`. `"1.0.0" == "1.0"`. Treat missing revisions as 0.

### Pseudocode
```text
FUNCTION compare_versions(v1, v2):
    SPLIT v1 by "." into list 'nums1'
    SPLIT v2 by "." into list 'nums2'
    
    DETERMINE max length 'L' between 'nums1' and 'nums2'
    
    FOR i FROM 0 TO L-1:
        GET val1 = integer at nums1[i] OR 0 if i is out of bounds
        GET val2 = integer at nums2[i] OR 0 if i is out of bounds
        
        IF val1 < val2: RETURN -1 (v1 is smaller)
        IF val1 > val2: RETURN 1  (v1 is larger)
        
    RETURN 0 (Versions are equal)
```

### Discussion & Tips
*   **The Trap:** Comparing strings directly (`"1.2" > "1.10"`) fails because "2" > "1" in ASCII. You *must* convert segments to integers.
*   **Padding:** The core trick is handling different lengths (`1.0` vs `1.0.1`). Treat the missing chunks as `0`.
*   **Zip Longest:** Python's `itertools.zip_longest(..., fillvalue=0)` is the "pro" way to implement the loop above.

---

## 5. Group Anagrams (HashMap Strategy)

**Problem:**  
Group a list of strings into anagrams.  
Input: `["eat", "tea", "tan", "ate", "nat", "bat"]`  
Output: `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`

### Pseudocode
```text
FUNCTION group_anagrams(word_list):
    INITIALIZE dictionary 'groups' (Key -> List)
    
    FOR EACH 'word' IN 'word_list':
        # Create a signature for the word
        # "eat" -> sort letters -> "aet"
        sorted_signature = SORT characters of 'word' and JOIN
        
        APPEND 'word' to groups[sorted_signature]
        
    RETURN values of 'groups' as a list
```

### Discussion & Tips
*   **Key Concept:** Anagrams contain the exact same characters. If you sort the characters, they become identical strings.
*   **Hash Map:** Using the sorted string as the Key allows O(1) lookups to find the correct bucket for the word.
*   **Complexity:** $O(N \cdot K \log K)$, where $N$ is number of words and $K$ is max length of a word (due to sorting each word).

---

## 6. Longest Substring Without Repeating Characters (Sliding Window)

**Problem:**  
Given a string, return the length of the longest substring with all unique characters.

### Pseudocode
```text
FUNCTION longest_unique_substring(s):
    INITIALIZE 'left' = 0
    INITIALIZE 'best' = 0
    INITIALIZE map 'last_seen' = empty

    FOR 'right' FROM 0 TO length(s) - 1:
        ch = s[right]

        IF ch IN last_seen AND last_seen[ch] >= left:
            left = last_seen[ch] + 1

        last_seen[ch] = right
        best = MAX(best, right - left + 1)

    RETURN best
```

### Discussion & Tips
*   **The Trap:** When you see a duplicate, you cannot move `left` backward. Use `MAX` logic to keep it monotonic.
*   **Why it Works:** The window `[left, right]` always contains unique characters.
*   **Complexity:** O(N) time, O(K) space for the map.

---

## 7. Minimum Window Substring (Advanced Sliding Window)

**Problem:**  
Given `s` and `t`, return the smallest substring of `s` that contains all characters in `t` (with correct counts). Return empty if none.

### Pseudocode
```text
FUNCTION min_window(s, t):
    IF t IS EMPTY: RETURN ""

    need = frequency map of chars in t
    missing = length(t)
    left = 0
    best_len = INFINITY
    best_range = (-1, -1)

    FOR right FROM 0 TO length(s) - 1:
        ch = s[right]
        IF ch IN need:
            need[ch] = need[ch] - 1
            IF need[ch] >= 0:
                missing = missing - 1

        WHILE missing == 0:
            IF (right - left + 1) < best_len:
                best_len = right - left + 1
                best_range = (left, right)

            left_ch = s[left]
            IF left_ch IN need:
                need[left_ch] = need[left_ch] + 1
                IF need[left_ch] > 0:
                    missing = missing + 1
            left = left + 1

    IF best_len == INFINITY: RETURN ""
    RETURN substring of s from best_range
```

### Discussion & Tips
*   **The Trap:** Counting `missing` based on total characters (not unique chars) avoids off-by-one errors.
*   **Key Insight:** Negative counts mean "extra" characters that can be dropped.
*   **Complexity:** O(N) time, O(K) space.

---

## 8. Number of Islands (Grid DFS/BFS)

**Problem:**  
Given a 2D grid of `"1"` (land) and `"0"` (water), count islands (connected land).

### Pseudocode
```text
FUNCTION num_islands(grid):
    IF grid IS EMPTY: RETURN 0
    rows = number of rows
    cols = number of cols
    count = 0

    FOR r FROM 0 TO rows - 1:
        FOR c FROM 0 TO cols - 1:
            IF grid[r][c] == "1":
                count = count + 1
                FLOOD_FILL(grid, r, c)

    RETURN count

FUNCTION flood_fill(grid, r, c):
    IF r OR c out of bounds: RETURN
    IF grid[r][c] != "1": RETURN

    grid[r][c] = "0"
    FOR EACH (dr, dc) IN [(1,0), (-1,0), (0,1), (0,-1)]:
        flood_fill(grid, r + dr, c + dc)
```

### Discussion & Tips
*   **Mutation:** Marking visited cells in-place avoids extra memory.
*   **Iterative Alternative:** Use a stack or queue to avoid recursion depth limits.
*   **Complexity:** O(R * C) time, O(R * C) worst-case space.

---

## 9. LRU Cache (Hash Map + Doubly Linked List)

**Problem:**  
Design an LRU Cache with `get` and `put` in O(1) time.

### Pseudocode
```text
CLASS Node:
    key, value
    prev, next

CLASS LRUCache(capacity):
    map = {}
    head = Node()  # dummy
    tail = Node()  # dummy
    head.next = tail
    tail.prev = head
    size = 0

    FUNCTION get(key):
        IF key NOT IN map: RETURN -1
        node = map[key]
        REMOVE(node)
        ADD_TO_FRONT(node)
        RETURN node.value

    FUNCTION put(key, value):
        IF key IN map:
            node = map[key]
            node.value = value
            REMOVE(node)
            ADD_TO_FRONT(node)
            RETURN

        IF size == capacity:
            lru = tail.prev
            REMOVE(lru)
            DELETE map[lru.key]
            size = size - 1

        node = Node(key, value)
        ADD_TO_FRONT(node)
        map[key] = node
        size = size + 1

    FUNCTION REMOVE(node):
        node.prev.next = node.next
        node.next.prev = node.prev

    FUNCTION ADD_TO_FRONT(node):
        node.next = head.next
        node.prev = head
        head.next.prev = node
        head.next = node
```

### Discussion & Tips
*   **Why Two Structures:** The map gives O(1) lookup; the list gives O(1) eviction order.
*   **The Trap:** You must move a node to the front on both `get` and `put`.

---

## 10. Kth Largest Element (Quickselect)

**Problem:**  
Find the Kth largest number in an unsorted array without sorting the full list.

### Pseudocode
```text
FUNCTION kth_largest(nums, k):
    target = length(nums) - k  # index if array were sorted ascending
    left = 0
    right = length(nums) - 1

    WHILE left <= right:
        pivot_index = PARTITION(nums, left, right)

        IF pivot_index == target: RETURN nums[pivot_index]
        ELSE IF pivot_index < target:
            left = pivot_index + 1
        ELSE:
            right = pivot_index - 1

FUNCTION PARTITION(nums, left, right):
    pivot = nums[right]
    store = left

    FOR i FROM left TO right - 1:
        IF nums[i] <= pivot:
            SWAP nums[i], nums[store]
            store = store + 1

    SWAP nums[store], nums[right]
    RETURN store
```

### Discussion & Tips
*   **Expected Time:** O(N) average, O(N^2) worst-case (mitigated by random pivot).
*   **The Trap:** Kth largest vs Kth smallest. Convert to index carefully.

---

## 11. Coin Change (Dynamic Programming)

**Problem:**  
Given coins and an amount, return the fewest coins needed, or `-1` if impossible.

### Pseudocode
```text
FUNCTION coin_change(coins, amount):
    dp = array of size amount + 1 filled with INFINITY
    dp[0] = 0

    FOR a FROM 1 TO amount:
        FOR coin IN coins:
            IF a - coin >= 0:
                dp[a] = MIN(dp[a], dp[a - coin] + 1)

    IF dp[amount] == INFINITY: RETURN -1
    RETURN dp[amount]
```

### Discussion & Tips
*   **Bottom-Up:** Each sub-amount builds on smaller solutions.
*   **Complexity:** O(amount * number_of_coins) time, O(amount) space.

---

## 12. Two Sum (Hash Map)

**Problem:**  
Given an array of integers and a target, return the indices of the two numbers that add up to the target.

### Pseudocode
```text
FUNCTION two_sum(nums, target):
    seen = empty map

    FOR i FROM 0 TO length(nums) - 1:
        need = target - nums[i]
        IF need IN seen:
            RETURN [seen[need], i]
        seen[nums[i]] = i

    RETURN []
```

### Discussion & Tips
*   **One-Pass:** The hash map stores what you have seen so far.
*   **The Trap:** You must insert after the check to avoid using the same element twice.

---

## 13. Valid Parentheses (Stack)

**Problem:**  
Given a string of brackets, determine if the order is valid.

### Pseudocode
```text
FUNCTION is_valid(s):
    stack = empty list
    pairs = {")": "(", "]": "[", "}": "{"}

    openers = SET of pairs values

    FOR ch IN s:
        IF ch IN pairs:
            IF stack IS EMPTY OR POP(stack) != pairs[ch]:
                RETURN False
        ELSE IF ch IN openers:
            PUSH ch TO stack

    RETURN stack IS EMPTY
```

### Discussion & Tips
*   **Core Idea:** Every closing bracket must match the most recent opening bracket.
*   **The Trap:** If the stack is empty when you see a closing bracket, fail immediately.

---

## 14. Product of Array Except Self (Prefix/Suffix)

**Problem:**  
Given an array, return a new array where each index has the product of all other elements.

### Pseudocode
```text
FUNCTION product_except_self(nums):
    n = length(nums)
    output = array of size n filled with 1

    prefix = 1
    FOR i FROM 0 TO n - 1:
        output[i] = prefix
        prefix = prefix * nums[i]

    suffix = 1
    FOR i FROM n - 1 DOWN TO 0:
        output[i] = output[i] * suffix
        suffix = suffix * nums[i]

    RETURN output
```

### Discussion & Tips
*   **No Division:** Handles zeros safely.
*   **Space:** O(1) extra space if you do not count the output array.

---

## 15. Merge Intervals (Sort + Merge)

**Problem:**  
Given intervals, merge any that overlap and return the consolidated list.

### Pseudocode
```text
FUNCTION merge_intervals(intervals):
    IF intervals IS EMPTY: RETURN []
    SORT intervals BY start

    merged = [intervals[0]]

    FOR current IN intervals[1:]:
        last = merged[-1]
        IF current.start <= last.end:
            last.end = MAX(last.end, current.end)
        ELSE:
            APPEND current TO merged

    RETURN merged
```

### Discussion & Tips
*   **Sorting is Mandatory:** Overlap checks only work after sorting by start.
*   **Pattern Link:** Same logic as merging maintenance windows.

---

## 16. Binary Search (Classic)

**Problem:**  
Given a sorted array, return the index of the target or `-1` if not found.

### Pseudocode
```text
FUNCTION binary_search(nums, target):
    left = 0
    right = length(nums) - 1

    WHILE left <= right:
        mid = left + ((right - left) // 2)
        IF nums[mid] == target: RETURN mid
        IF nums[mid] < target:
            left = mid + 1
        ELSE:
            right = mid - 1

    RETURN -1
```

### Discussion & Tips
*   **Overflow Safe:** `left + (right - left) // 2` avoids integer overflow in other languages.
*   **The Trap:** Use `<=` in the loop or you will skip the last element.

---

## 17. Subarray Sum Equals K (Prefix Sum + Hash Map)

**Problem:**  
Given an array and integer `k`, count the number of subarrays that sum to `k`.

### Pseudocode
```text
FUNCTION subarray_sum(nums, k):
    count = 0
    prefix = 0
    freq = map with {0: 1}

    FOR num IN nums:
        prefix = prefix + num
        count = count + freq.get(prefix - k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1

    RETURN count
```

### Discussion & Tips
*   **Key Insight:** If `prefix[j] - prefix[i] = k`, then subarray `(i+1..j)` sums to `k`.
*   **The Trap:** Initialize `{0: 1}` to count subarrays that start at index 0.
