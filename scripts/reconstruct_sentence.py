
def reconstruct_sentence(part1, part2):
    # Combine the lists
    combined_list = part1 + part2
    
    parsed_words = []
    
    for item in combined_list:
        # Split by the first colon found
        if ':' in item:
            index_str, word = item.split(':', 1)
            # Strip whitespace and convert index to integer
            try:
                index = int(index_str.strip())
                word = word.strip()
                parsed_words.append((index, word))
            except ValueError:
                print(f"Skipping invalid item format: {item}")
    
    # Sort based on the index (first element of tuple)
    parsed_words.sort(key=lambda x: x[0])
    
    # Extract just the words
    words = [word for _, word in parsed_words]
    
    # Join them with spaces and append the period
    result = " ".join(words) + "."
    return result

if __name__ == "__main__":
    part_1 = [" 9: dog ", " 2 :quick ", "4: fox", " 7: the ", "5: jumps"]
    part_2 = ["3 :brown", " 1 : the", " 6:over", "8 :lazy", "10: this", " 11 : morning"]
    
    sentence = reconstruct_sentence(part_1, part_2)
    print(sentence)
