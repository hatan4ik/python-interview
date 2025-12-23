
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
