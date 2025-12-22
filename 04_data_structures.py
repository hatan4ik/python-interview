#!/usr/bin/env python3
"""
Data Structures & Efficiency.

This module highlights the performance differences between Python data structures.
Key takeaway: Sets provide O(1) lookups, while Lists provide O(N).
"""

from typing import List, Set, TypedDict

# User definition for strong typing
class User(TypedDict):
    name: str
    age: int
    role: str

def list_vs_set_efficiency() -> None:
    """
    Demonstrates finding common elements (Intersection).
    
    Performance Note:
        - List Intersection: O(N * M)
        - Set Intersection:  O(min(N, M)) -> Significantly faster for large data.
    """
    print("--- 1. Set Intersection (Common Elements) ---")
    
    dc1_servers: List[str] = ["server-alpha", "server-beta", "server-gamma", "server-delta"]
    dc2_servers: List[str] = ["server-beta", "server-epsilon", "server-delta", "server-zeta"]
    
    set1: Set[str] = set(dc1_servers)
    set2: Set[str] = set(dc2_servers)
    
    # intersection() is optimized in C
    common = set1 & set2
    
    print(f"Servers in both lists: {common}")

def sorting_dictionaries() -> None:
    """
    Demonstrates sorting a list of dictionaries by a specific key.
    Uses 'lambda' functions, a common interview requirement.
    """
    print("\n--- 2. Sorting Dictionaries ---")
    
    users: List[User] = [
        {"name": "Alice", "age": 30, "role": "DevOps"},
        {"name": "Bob", "age": 25, "role": "Developer"},
        {"name": "Charlie", "age": 35, "role": "Manager"}
    ]
    
    # Sort in-place would use .sort(), but sorted() returns a new list
    sorted_users = sorted(users, key=lambda x: x['age'])
    
    print("Users sorted by age:")
    for u in sorted_users:
        print(f"  {u['name']}: {u['age']}")

def cleaning_data() -> None:
    """
    Demonstrates data cleaning using Set Comprehensions.
    Removes duplicates and normalizes whitespace/casing in one pass.
    """
    print("\n--- 3. List Comprehensions & Cleaning ---")
    
    raw_tags: List[str] = [" PROD ", "dev", "Test", "PROD", "  dev  ", "staging"]
    
    # Set comprehension {} automatically handles deduplication
    cleaned_tags: Set[str] = {tag.strip().lower() for tag in raw_tags} 
    
    print(f"Raw tags: {raw_tags}")
    print(f"Cleaned unique tags: {cleaned_tags}")

if __name__ == "__main__":
    list_vs_set_efficiency()
    sorting_dictionaries()
    cleaning_data()
