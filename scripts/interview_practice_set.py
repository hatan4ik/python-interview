
import collections

def problem_1_reorder_log_files(logs):
    """
    Problem: Reorder Log Files (Classic Amazon/FAANG)
    
    Input: List of strings. Each string is a space-delimited log.
    - The first word is the "identifier".
    - The rest is the "content".
    
    Rules:
    1. "Letter-logs": Content consists of lowercase English letters.
    2. "Digit-logs": Content consists of digits.
    3. Letter-logs come before all digit-logs.
    4. Letter-logs are sorted lexicographically by their content. 
       If content is the same, sort by identifier.
    5. Digit-logs maintain their original relative order (stable sort).
    
    Interview Tip:
    - This tests your ability to write a custom sort key.
    - Python's sort is stable, which makes rule #5 easy if you just separate them.
    """
    letters = []
    digits = []
    
    for log in logs:
        # Split into [identifier, content]
        # maxsplit=1 is crucial here to keep the content as a single string
        identifier, content = log.split(" ", 1)
        
        # Check if the first character of the content is a digit
        if content[0].isdigit():
            digits.append(log)
        else:
            # We store (content, identifier, original_log) to make sorting easy
            letters.append((content, identifier, log))
            
    # Sort letters: primary key = content, secondary key = identifier
    letters.sort(key=lambda x: (x[0], x[1]))
    
    # Extract the original string back
    sorted_letters = [x[2] for x in letters]
    
    # Concatenate: letters first, then digits
    return sorted_letters + digits


def problem_2_group_anagrams(strs):
    """
    Problem: Group Anagrams
    
    Input: List of strings ["eat", "tea", "tan", "ate", "nat", "bat"]
    Output: Grouped list [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    
    Interview Tip:
    - Brute force is O(N^2). We need O(N * K log K) or O(N * K).
    - The key observation: "eat" and "tea" sort to the same string "aet".
    - Use a HashMap (dictionary) where Key = sorted string, Value = list of original strings.
    """
    anagram_map = collections.defaultdict(list)
    
    for word in strs:
        # Strings are immutable, so we sort it into a list, then join or tuple it to make it a dict key
        # "eat" -> ['a', 'e', 't'] -> "aet"
        sorted_key = "".join(sorted(word))
        anagram_map[sorted_key].append(word)
        
    return list(anagram_map.values())


def problem_3_longest_substring_without_repeating(s):
    """
    Problem: Longest Substring Without Repeating Characters
    
    Input: "abcabcbb" -> Output: 3 ("abc")
    Input: "pwwkew" -> Output: 3 ("wke")
    
    Interview Tip:
    - "Sliding Window" technique.
    - Keep a 'left' pointer and a 'right' pointer.
    - Use a dictionary to track the LAST seen index of each character.
    - If you see a duplicate, jump the 'left' pointer ahead.
    """
    used_char_map = {}
    max_length = 0
    left_pointer = 0
    
    for right_pointer, char in enumerate(s):
        # If we have seen this char AND it is inside our current window
        if char in used_char_map and used_char_map[char] >= left_pointer:
            # Move the left pointer to just after the last occurrence
            left_pointer = used_char_map[char] + 1
        else:
            # Update max length
            current_len = right_pointer - left_pointer + 1
            max_length = max(max_length, current_len)
            
        # Update the last seen index of the char
        used_char_map[char] = right_pointer
        
    return max_length


def problem_4_two_sum(nums, target):
    """
    Problem: Two Sum

    Input: nums = [2, 7, 11, 15], target = 9
    Output: [0, 1]

    Interview Tip:
    - Use a hash map to store complements.
    - One-pass solution is O(N).
    """
    seen = {}

    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return [seen[need], i]
        seen[num] = i

    return []


def problem_5_valid_parentheses(s):
    """
    Problem: Valid Parentheses

    Input: "()[]{}" -> True
    Input: "(]" -> False

    Interview Tip:
    - Stack is the only sane choice.
    - If you see a closing bracket with an empty stack, fail immediately.
    """
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    opens = set(pairs.values())

    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        elif ch in opens:
            stack.append(ch)
        else:
            continue

    return not stack


def problem_6_product_except_self(nums):
    """
    Problem: Product of Array Except Self

    Input: [1, 2, 3, 4]
    Output: [24, 12, 8, 6]

    Interview Tip:
    - Use prefix and suffix products (no division).
    - O(N) time, O(1) extra space (excluding output).
    """
    n = len(nums)
    output = [1] * n

    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]

    return output


def problem_7_merge_intervals(intervals):
    """
    Problem: Merge Intervals

    Input: [[1,3], [2,6], [8,10], [15,18]]
    Output: [[1,6], [8,10], [15,18]]

    Interview Tip:
    - Sort by start, then merge greedily.
    - Note: This sorts the input list in place.
    """
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)

    return merged


def problem_8_binary_search(nums, target):
    """
    Problem: Binary Search

    Input: nums = [1, 3, 5, 7, 9], target = 7
    Output: 3
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def problem_9_subarray_sum_equals_k(nums, k):
    """
    Problem: Subarray Sum Equals K

    Input: nums = [1, 1, 1], k = 2
    Output: 2

    Interview Tip:
    - Prefix sum + frequency map.
    """
    count = 0
    prefix = 0
    freq = {0: 1}

    for num in nums:
        prefix += num
        count += freq.get(prefix - k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1

    return count


def problem_10_number_of_islands(grid):
    """
    Problem: Number of Islands

    Input:
    [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    Output: 3

    Note: This mutates the grid to mark visited cells.
    """
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != "1":
            return
        grid[r][c] = "0"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)

    return count


if __name__ == "__main__":
    print("--- Problem 1: Reorder Log Files ---")
    logs = ["dig1 8 1 5 1", "let1 art can", "dig2 3 6", "let2 own kit dig", "let3 art zero"]
    print(f"Input: {logs}")
    print(f"Output: {problem_1_reorder_log_files(logs)}")
    print("\n")
    
    print("--- Problem 2: Group Anagrams ---")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"Input: {words}")
    print(f"Output: {problem_2_group_anagrams(words)}")
    print("\n")
    
    print("--- Problem 3: Longest Substring Without Repeating Chars ---")
    s = "abcabcbb"
    print(f"Input: {s}")
    print(f"Output: {problem_3_longest_substring_without_repeating(s)}")
    print("\n")

    print("--- Problem 4: Two Sum ---")
    nums = [2, 7, 11, 15]
    target = 9
    print(f"Input: nums={nums}, target={target}")
    print(f"Output: {problem_4_two_sum(nums, target)}")
    print("\n")

    print("--- Problem 5: Valid Parentheses ---")
    s = "()[]{}"
    print(f"Input: {s}")
    print(f"Output: {problem_5_valid_parentheses(s)}")
    print("\n")

    print("--- Problem 6: Product Except Self ---")
    nums = [1, 2, 3, 4]
    print(f"Input: {nums}")
    print(f"Output: {problem_6_product_except_self(nums)}")
    print("\n")

    print("--- Problem 7: Merge Intervals ---")
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(f"Input: {intervals}")
    print(f"Output: {problem_7_merge_intervals(intervals)}")
    print("\n")

    print("--- Problem 8: Binary Search ---")
    nums = [1, 3, 5, 7, 9]
    target = 7
    print(f"Input: nums={nums}, target={target}")
    print(f"Output: {problem_8_binary_search(nums, target)}")
    print("\n")

    print("--- Problem 9: Subarray Sum Equals K ---")
    nums = [1, 1, 1]
    k = 2
    print(f"Input: nums={nums}, k={k}")
    print(f"Output: {problem_9_subarray_sum_equals_k(nums, k)}")
    print("\n")

    print("--- Problem 10: Number of Islands ---")
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    print("Input: grid=4x5")
    print(f"Output: {problem_10_number_of_islands(grid)}")
