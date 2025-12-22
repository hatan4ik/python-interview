# ==========================================
# SCENARIO:
# 1. You have two lists of server hostnames. Find the ones present in both (intersection).
# 2. You have a list of user dictionaries. Sort them by age.
# 3. Clean a list of tags (remove duplicates and normalize case).
# ==========================================

def list_vs_set_efficiency():
    print("--- 1. Set Intersection (Common Elements) ---")
    
    # Imagine these are huge lists from two different data centers
    dc1_servers = ["server-alpha", "server-beta", "server-gamma", "server-delta"]
    dc2_servers = ["server-beta", "server-epsilon", "server-delta", "server-zeta"]
    
    # BAD WAY (O(n*m) complexity - Slow):
    # common = []
    # for s1 in dc1_servers:
    #     if s1 in dc2_servers:
    #         common.append(s1)
            
    # GOOD WAY (O(n+m) complexity - Fast):
    set1 = set(dc1_servers)
    set2 = set(dc2_servers)
    
    common = set1.intersection(set2)
    # OR simpler syntax: common = set1 & set2
    
    print(f"Servers in both lists: {common}")

def sorting_dictionaries():
    print("\n--- 2. Sorting Dictionaries ---")
    
    users = [
        {"name": "Alice", "age": 30, "role": "DevOps"},
        {"name": "Bob", "age": 25, "role": "Developer"},
        {"name": "Charlie", "age": 35, "role": "Manager"}
    ]
    
    # Sort by 'age' key
    # Key concept: Lambda functions
    sorted_users = sorted(users, key=lambda x: x['age'])
    
    print("Users sorted by age:")
    for u in sorted_users:
        print(f"  {u['name']}: {u['age']}")

def cleaning_data():
    print("\n--- 3. List Comprehensions & Cleaning ---")
    
    raw_tags = [" PROD ", "dev", "Test", "PROD", "  dev  ", "staging"]
    
    # Goal: ['prod', 'dev', 'test', 'staging'] (Cleaned and Unique)
    
    # List Comprehension: [expression for item in list]
    cleaned_tags = {tag.strip().lower() for tag in raw_tags} 
    # Note: using {} creates a SET directly (unique), [] creates a LIST.
    
    print(f"Raw tags: {raw_tags}")
    print(f"Cleaned unique tags: {cleaned_tags}")

if __name__ == "__main__":
    list_vs_set_efficiency()
    sorting_dictionaries()
    cleaning_data()
