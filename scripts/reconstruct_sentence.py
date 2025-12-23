def reconstruct_sentence(part1, part2):
    """
    Reconstructs a sentence from two lists of scrambled words with indices.
    
    Interview Tips:
    1. Handling input: Combine sources first.
    2. String Parsing: The format "<index>:<word>" is tricky because of whitespace.
       - " 2 :quick " -> split(':') might give [" 2 ", "quick "]
       - crucial to use .strip() on both sides.
    3. Sorting: Store as tuples (index, word) and sort by index.
    """
    
    # 1. Combine the data sources
    combined_list = part1 + part2
    
    parsed_words = []
    
    for item in combined_list:
        # 2. Parse the string
        # split(':', 1) ensures we only split on the separator, just in case the word has a colon (unlikely here but good safety)
        if ':' in item:
            index_str, word = item.split(':', 1)
            
            # CRITICAL STEP: Sanitize the data
            # " 9" -> 9
            # " dog " -> "dog"
            try:
                index = int(index_str.strip())
                word = word.strip()
                parsed_words.append((index, word))
            except ValueError:
                print(f"Skipping invalid item: {item}")
    
    # 3. Sort the data
    # Python's sort is stable and efficient (Timsort). 
    # We sort by the first element of the tuple (the index).
    parsed_words.sort(key=lambda x: x[0])
    
    # 4. Construct the output
    # List comprehensions are preferred in Python interviews for this extraction step
    final_words = [word for _, word in parsed_words]
    
    # Join with space and add the period as requested
    result = " ".join(final_words) + "."
    return result

if __name__ == "__main__":
    # Test Data
    part_1 = [" 9: dog ", " 2 :quick ", "4: fox", " 7: the ", "5: jumps"]
    part_2 = ["3 :brown", " 1 : the", " 6:over", "8 :lazy", "10: this", " 11 : morning"]
    
    print(f"Input 1: {part_1}")
    print(f"Input 2: {part_2}")
    print("-" * 20)
    
    sentence = reconstruct_sentence(part_1, part_2)
    print(f"Output: {sentence}")