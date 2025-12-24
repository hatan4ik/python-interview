
def luhn_check(card_number):
    """
    Classic Interview Algo: The Luhn Algorithm (Mod 10).
    Used to validate credit card numbers, IMEI numbers, etc.
    
    Rules:
    1. Drop the last digit (check digit).
    2. Reverse the numbers.
    3. Multiply digits at odd indices (0, 2, 4...) by 2.
    4. If the result is > 9, subtract 9 (e.g., 8*2=16 -> 7).
    5. Sum all numbers.
    6. (Sum * 9) % 10 should equal the check digit.
    
    *Simplified Variation often used in interviews:*
    1. Double every second digit from the right.
    2. Sum all digits (if double > 9, sum the digits of the result, e.g., 16 -> 1+6=7).
    3. If total % 10 == 0, it's valid.
    """
    # 1. Convert string to list of integers
    # "1234" -> [1, 2, 3, 4]
    try:
        digits = [int(d) for d in str(card_number)]
    except ValueError:
        return False

    # 2. Iterate backwards, skipping the last one (check digit) if you want to calculate it,
    #    OR just process the whole thing to check validity.
    #    Let's check validity of the FULL number.
    
    checksum = 0
    # Iterate backwards using range(start, stop, step)
    # Start at second to last digit, go to 0, step -2 (doubling digits)
    # Then sum the rest.
    
    # Actually, a cleaner pythonic way for the loop:
    # Reverse it first
    digits = digits[::-1]
    
    for i, d in enumerate(digits):
        if i % 2 == 1: # Every second digit (since we are 0-indexed)
            doubled = d * 2
            if doubled > 9:
                doubled -= 9 # Same as summing digits of a number < 20
            checksum += doubled
        else:
            checksum += d
            
    return checksum % 10 == 0

def get_issuer(card_number):
    """
    Identify card network based on prefixes.
    """
    s = str(card_number)
    if s.startswith('4'):
        return 'Visa'
    elif 51 <= int(s[:2]) <= 55:
        return 'Mastercard'
    elif s.startswith(('34', '37')):
        return 'Amex'
    return 'Unknown'

def mask_number(card_number):
    """
    Return format: ************1234
    """
    s = str(card_number)
    if len(s) < 4:
        return s
    return '*' * (len(s) - 4) + s[-4:]

def process_batch(raw_transactions):
    """
    Scenario:
    You receive a list of messy transaction strings like " 4111-2222-3333-4444 ".
    
    Task:
    1. Clean the input (remove spaces, dashes).
    2. Filter out invalid cards (Luhn check fails).
    3. Return a list of valid transactions sorted by:
       - Issuer (Alphabetical: Amex -> Mastercard -> Visa)
       - Then by Last 4 digits (Descending)
    """
    valid_cards = []
    
    for raw in raw_transactions:
        # 1. Clean data
        clean_num = raw.replace('-', '').replace(' ', '').strip()
        
        # Validate content is numeric
        if not clean_num.isdigit():
            print(f"Skipping non-numeric: {raw}")
            continue
            
        # 2. Validate Algo
        if luhn_check(clean_num):
            issuer = get_issuer(clean_num)
            masked = mask_number(clean_num)
            # Store tuple for sorting: (Issuer, Last4, Original_Clean)
            # Storing 'clean_num' integer for secondary sort if needed, 
            # but request asked for Last 4.
            valid_cards.append({
                'issuer': issuer,
                'masked': masked,
                'full_num': clean_num
            })
        else:
            print(f"Invalid Checksum: {clean_num}")

    # 3. Sorting with complex keys
    # Primary: Issuer (Ascending)
    # Secondary: Last 4 digits (Descending) -> We use negative int for desc sort shortcut
    # Python sort key: (Issuer, -int(last_4))
    
    valid_cards.sort(key=lambda x: (x['issuer'], -int(x['full_num'][-4:])))
    
    return valid_cards

if __name__ == "__main__":
    # Test Data
    # 424242... is a standard Stripe test Visa
    # 5555... is Mastercard
    # 3782... is Amex
    # 4111...1112 is a fake/bad number for luhn check
    input_data = [
        " 4242-4242-4242-4242 ", # Valid Visa
        "5555555555554444",       # Valid MC
        "378282246310005",        # Valid Amex
        "4242 4242 4242 9999",    # Valid Visa (higher last 4 than first one)
        "4111111111111112",       # Invalid Luhn (ends in 2 instead of 1)
        "abc-123",                # Garbage
    ]
    
    print("--- Raw Batch ---")
    print(input_data)
    print("\n--- Processing ---")
    
    results = process_batch(input_data)
    
    print("\n--- Sorted Valid Results ---")
    for res in results:
        print(f"[{res['issuer']}] {res['masked']}")
