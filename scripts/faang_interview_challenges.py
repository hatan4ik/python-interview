"""
FAANG INTERVIEW CHALLENGES (The "Bar Raisers")
---------------------------------------------
Author: Aaron Maxwell (Persona)
Context: Systems Design & Hard Algo Implementation for SRE/DevOps

These questions bridge the gap between "Algorithms" and "Systems".
They test if you can write efficient code for practical Ops problems.

CHALLENGES:
1. Rate Limiter (Sliding Window Log)
2. Merge K Sorted Log Streams (Heap)
3. Valid Configuration Brackets (Stack)
4. Top K Frequent IPs (Counter + Heap)
5. Service Tree Serialization (DFS/Recursion)
"""

import heapq
import collections
import time
from collections import deque

# ==========================================
# 1. RATE LIMITER (Sliding Window Log)
# ==========================================
class RateLimiter:
    """
    Problem: Design a rate limiter that allows N requests per M seconds.
    Constraint: High accuracy required (not just "fixed window").
    
    Strategy: Sliding Window Log.
    - Store timestamps of successful requests in a Queue (Deque).
    - On new request, remove timestamps older than (Now - M).
    - If len(queue) < N, allow. Else, reject.
    """
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = deque()

    def allow_request(self, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
            
        # 1. Clean up old requests (Slide the window)
        # While the oldest request is outside the window...
        while self.requests and self.requests[0] <= timestamp - self.window_seconds:
            self.requests.popleft()
            
        # 2. Check Capacity
        if len(self.requests) < self.limit:
            self.requests.append(timestamp)
            return True
        
        return False

# ==========================================
# 2. MERGE K SORTED LOG STREAMS (Heap)
# ==========================================
def merge_k_logs(log_files):
    """
    Problem: You have K huge log files. Each is sorted by timestamp.
    Merge them into one single sorted output stream.
    
    Constraint: You cannot load all files into RAM.
    
    Strategy: Min-Heap.
    - Put the first line of each file into a Min-Heap: (timestamp, line, file_index).
    - Pop the smallest item (earliest timestamp). Write to output.
    - Read the next line from the file that just "won" and push to Heap.
    - Repeat until Heap is empty.
    
    Complexity: O(N log K) where N is total lines, K is number of files.
    """
    min_heap = []
    
    # 1. Initialize Heap with first line from each list
    # Input format: List of Lists of LogEntry(timestamp, message)
    # We simulate file reading with iterators
    iterators = [iter(logs) for logs in log_files]
    
    for i, it in enumerate(iterators):
        try:
            entry = next(it) # format: (timestamp, message)
            # Heap Tuple: (timestamp, unique_id, message, file_index)
            # We add 'i' (file_index) as tie-breaker so we don't compare messages
            heapq.heappush(min_heap, (entry[0], i, entry[1]))
        except StopIteration:
            continue
            
    merged_output = []
    
    while min_heap:
        timestamp, file_idx, message = heapq.heappop(min_heap)
        merged_output.append((timestamp, message))
        
        # 2. Fetch next from the same source
        try:
            next_entry = next(iterators[file_idx])
            heapq.heappush(min_heap, (next_entry[0], file_idx, next_entry[1]))
        except StopIteration:
            continue
            
    return merged_output

# ==========================================
# 3. VALID CONFIGURATION BRACKETS (Stack)
# ==========================================
def validate_config_brackets(config_str):
    """
    Problem: Validate JSON/Terraform-like brackets: {}, [], ().
    Input: "{ var = [ (a + b) ] }" -> Valid
    Input: "{ var = [ (a + b ) }" -> Invalid (Missing ']')
    
    Strategy: Stack.
    - Open bracket? Push to stack.
    - Close bracket? Check if stack top matches.
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in config_str:
        if char in mapping.values(): # Openers: (, {, [
            stack.append(char)
        elif char in mapping: # Closers: ), }, ]
            if not stack or stack.pop() != mapping[char]:
                return False
                
    return len(stack) == 0

# ==========================================
# 4. TOP K FREQUENT IPS (Counter + Heap)
# ==========================================
def top_k_ips(ip_stream, k):
    """
    Problem: Find the top K most frequent IP addresses in a stream.
    
    Strategy: 
    1. Count frequencies (HashMap).
    2. Use Heap (heapq.nlargest) to get top K.
    """
    # collections.Counter is O(N) optimized C-hashing
    counts = collections.Counter(ip_stream)
    
    # heapq.nlargest is O(N log K) - better than sorting O(N log N)
    # It keeps a min-heap of size K
    return heapq.nlargest(k, counts.keys(), key=counts.get)

# ==========================================
# 5. SERVICE TREE SERIALIZATION (Recursion)
# ==========================================
class ServiceNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children else []

class Codec:
    """
    Problem: Serialize a Service Dependency Tree to a string and deserialize it back.
    Format: "Name(Child1,Child2(Grandchild))" or similar.
    Let's use a simpler JSON-like pre-order format: "Name [Child1 [ ... ] Child2 [] ]"
    """
    def serialize(self, root):
        """Encodes a tree to a single string."""
        if not root: return ""
        
        # Pre-order DFS: Root, then Children
        res = [root.name]
        
        # Add a marker for number of children or just recurse
        # Strategy: "Name ( Child1Val Child2Val )"
        # Let's use a flat list approach with markers or JSON. 
        # Standard Interview Algo: "1,2,x,x,3,x,x" (Pre-order with Nulls) doesn't work well for N-ary.
        # N-ary approach: Name, SizeOfChildren, Child1, Child2...
        
        res.append(str(len(root.children)))
        for child in root.children:
            res.append(self.serialize(child))
            
        return ",".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        if not data: return None
        
        queue = collections.deque(data.split(','))
        
        def helper():
            if not queue: return None
            
            name = queue.popleft()
            if not name: return None # Handle potential empty split
            
            size_str = queue.popleft()
            size = int(size_str)
            
            node = ServiceNode(name)
            for _ in range(size):
                node.children.append(helper())
            return node
            
        return helper()

# ==========================================
# MAIN EXECUTION & TESTS
# ==========================================
if __name__ == "__main__":
    print("--- 1. Rate Limiter ---")
    limiter = RateLimiter(limit=2, window_seconds=1)
    print(f"Req 1 (0.0s): {limiter.allow_request(0.1)}") # True
    print(f"Req 2 (0.2s): {limiter.allow_request(0.2)}") # True
    print(f"Req 3 (0.3s): {limiter.allow_request(0.3)}") # False (Max 2 per 1s)
    print(f"Req 4 (1.2s): {limiter.allow_request(1.2)}") # True (0.1 expired)
    
    print("\n--- 2. Merge K Logs ---")
    log1 = [(1, "A"), (3, "B"), (5, "C")]
    log2 = [(2, "D"), (4, "E")]
    log3 = [(0, "Start")]
    print(f"Merged: {merge_k_logs([log1, log2, log3])}")
    
    print("\n--- 3. Valid Config ---")
    print(f"{{ [ ( ) ] }}: {validate_config_brackets('{ [ ( ) ] }')}")
    print(f"{{ [ ( ) ] ] }}: {validate_config_brackets('{ [ ( ) ] ] }')}")
    
    print("\n--- 4. Top K IPs ---")
    ips = ["1.1.1.1", "2.2.2.2", "1.1.1.1", "3.3.3.3", "2.2.2.2", "1.1.1.1"]
    print(f"Stream: {ips}")
    print(f"Top 2: {top_k_ips(ips, 2)}")
    
    print("\n--- 5. Service Tree ---")
    # Tree: Gateway -> (Auth, Payment)
    root = ServiceNode("Gateway", [ServiceNode("Auth"), ServiceNode("Payment")])
    codec = Codec()
    serialized = codec.serialize(root)
    print(f"Serialized: {serialized}")
    deserialized = codec.deserialize(serialized)
    print(f"Deserialized Children: {[c.name for c in deserialized.children]}")
