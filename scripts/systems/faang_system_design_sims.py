"""
FAANG SYSTEM DESIGN SIMULATIONS
-------------------------------
Author: Aaron Maxwell (Persona)
Context: Coding the components of a Distributed System.

Don't just draw boxes on a whiteboard. Code the logic inside the box.

COMPONENTS:
1. TRIE (Prefix Tree) - The engine behind "Google Search Autocomplete".
2. CONSISTENT HASHING - The algorithm behind Cassandra/DynamoDB Partitioning.
3. LOAD BALANCER (Round Robin & Least Connection).
"""

import hashlib
import bisect

# ==========================================
# 1. TRIE (Autocomplete Engine)
# ==========================================
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0 # For ranking results

class Trie:
    """
    Data Structure for O(L) lookup of words, where L is word length.
    Crucial for Typeahead/Autocomplete.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            # Optimization: We could store top-k words at every node for O(1) autocomplete
        node.is_end_of_word = True
        node.frequency += 1

    def search_prefix(self, prefix):
        """Returns all words starting with prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # DFS to find all words below this node
        results = []
        self._dfs(node, prefix, results)
        return results

    def _dfs(self, node, current_prefix, results):
        if node.is_end_of_word:
            results.append(current_prefix)
        
        for char, child_node in node.children.items():
            self._dfs(child_node, current_prefix + char, results)

# ==========================================
# 2. CONSISTENT HASHING RING
# ==========================================
class ConsistentHashRing:
    """
    Problem: Distribute keys across N servers.
    Challenge: If a server dies, we don't want to re-hash ALL keys. 
               Only keys from the dead server should move.
               
    Solution: Hash servers and keys onto a circle (0 - 2^32).
    """
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas # Virtual nodes to balance load
        self.ring = {} # Map Hash -> Node Name
        self.sorted_keys = [] # Sorted Hash values
        
        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key):
        """Returns MD5 hash as integer."""
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            bisect.insort(self.sorted_keys, key)

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key_string):
        if not self.ring: return None
        
        hash_val = self._hash(key_string)
        
        # Find the first node clockwise from hash_val
        idx = bisect.bisect_right(self.sorted_keys, hash_val)
        
        # Wrap around if at the end of the ring
        if idx == len(self.sorted_keys):
            idx = 0
            
        return self.ring[self.sorted_keys[idx]]

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    print("--- 1. TRIE AUTOCOMPLETE ---")
    trie = Trie()
    for word in ["apple", "app", "apricot", "banana", "bat"]:
        trie.insert(word)
    
    print(f"Prefix 'ap': {trie.search_prefix('ap')}")
    print(f"Prefix 'ba': {trie.search_prefix('ba')}")
    
    print("\n--- 2. CONSISTENT HASHING ---")
    servers = ["Server-A", "Server-B", "Server-C"]
    ring = ConsistentHashRing(servers)
    
    users = ["User1", "User2", "User3", "User4", "User5"]
    print("Initial Distribution:")
    for u in users:
        print(f"  {u} -> {ring.get_node(u)}")
        
    print("\n[!] Server-A Crashes...")
    ring.remove_node("Server-A")
    
    print("New Distribution (Note minimal movement):")
    for u in users:
        print(f"  {u} -> {ring.get_node(u)}")
