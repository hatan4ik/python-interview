# Python Interview: Pseudocode & Algorithms Guide

This guide covers common "string manipulation and sorting" interview questions, providing **Pseudocode**, **Pythonic Logic**, and **Discussion** for each.

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
