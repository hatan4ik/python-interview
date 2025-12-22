from typing import List, Set, TypedDict

# ==========================================
# SCENARIO:
# Data Structures with TypedDict for structure definition.
# ==========================================

# MODERN: TypedDict (Python 3.8+)
# Defines the expected keys and value types for a dictionary.
class User(TypedDict):
    name: str
    age: int
    role: str

def list_vs_set_efficiency() -> None:
    print("--- 1. Set Intersection (Common Elements) ---")
    
    dc1_servers: List[str] = ["server-alpha", "server-beta", "server-gamma", "server-delta"]
    dc2_servers: List[str] = ["server-beta", "server-epsilon", "server-delta", "server-zeta"]
    
    # Type inference works well here, but explicit hints show intent
    set1: Set[str] = set(dc1_servers)
    set2: Set[str] = set(dc2_servers)
    
    # O(min(len(s1), len(s2))) complexity
    common = set1 & set2
    
    print(f"Servers in both lists: {common}")

def sorting_dictionaries() -> None:
    print("\n--- 2. Sorting Dictionaries ---")
    
    # The type hint 'List[User]' validates the structure of the dicts inside
    users: List[User] = [
        {"name": "Alice", "age": 30, "role": "DevOps"},
        {"name": "Bob", "age": 25, "role": "Developer"},
        {"name": "Charlie", "age": 35, "role": "Manager"}
    ]
    
    sorted_users = sorted(users, key=lambda x: x['age'])
    
    print("Users sorted by age:")
    for u in sorted_users:
        print(f"  {u['name']}: {u['age']}")

def cleaning_data() -> None:
    print("\n--- 3. List Comprehensions & Cleaning ---")
    
    raw_tags: List[str] = [" PROD ", "dev", "Test", "PROD", "  dev  ", "staging"]
    
    # Set comprehension for unique values
    cleaned_tags: Set[str] = {tag.strip().lower() for tag in raw_tags} 
    
    print(f"Raw tags: {raw_tags}")
    print(f"Cleaned unique tags: {cleaned_tags}")

if __name__ == "__main__":
    list_vs_set_efficiency()
    sorting_dictionaries()
    cleaning_data()