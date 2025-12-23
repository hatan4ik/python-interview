# Advanced DevOps & Python Interview Algorithms
*Level: Senior DevOps Engineer / Principal DevOps / Senior Python Developer*

This guide focuses on **System Design in Code** and **Algorithmic Operations** relevant to infrastructure, CI/CD, and reliability engineering.

---

## 1. The "Build Order" (Dependency Resolution)
**Context:** You have a list of microservices and their dependencies (e.g., in a `docker-compose` or Terraform dependency graph).
**Goal:** Return a list of services in the order they must be started/built. If a cycle exists (A->B->A), detect it.

### Pseudocode (Kahn's Algorithm / Topological Sort)
```text
FUNCTION get_build_order(services, dependencies):
    # 1. Initialize Graph and In-Degree Counter
    graph = {service: []}
    in_degree = {service: 0}
    
    # 2. Build the Graph
    FOR EACH (dependant, dependency) IN dependencies:
        APPEND dependant TO graph[dependency]
        INCREMENT in_degree[dependant]
        
    # 3. Find services with NO dependencies (Start nodes)
    queue = [service WHERE in_degree[service] == 0]
    build_order = []
    
    # 4. Process the queue
    WHILE queue IS NOT EMPTY:
        current = POP from queue
        APPEND current TO build_order
        
        # "Remove" this node, reduce neighbor in-degrees
        FOR neighbor IN graph[current]:
            DECREMENT in_degree[neighbor]
            IF in_degree[neighbor] == 0:
                PUSH neighbor TO queue
                
    # 5. Cycle Detection
    IF length(build_order) != length(services):
        RAISE Error "Circular Dependency Detected"
        
    RETURN build_order
```

### Python Implementation
```python
from collections import defaultdict, deque

def resolve_dependencies(services, deps):
    # deps is list of tuples: ('backend', 'db') -> backend depends on db
    # Graph: nodes point to things that depend on them (db -> backend)
    graph = defaultdict(list)
    in_degree = {s: 0 for s in services}
    
    for dependant, provider in deps:
        graph[provider].append(dependant)
        in_degree[dependant] += 1
        
    # Queue of nodes ready to be processed
    queue = deque([node for node in services if in_degree[node] == 0])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(order) != len(services):
        raise ValueError("Cycle detected! Circular dependencies exist.")
        
    return order
```

---

## 2. Sliding Window Log Analysis (DDoS Detection)
**Context:** You have a stream of access logs. You need to identify if any IP address has exceeded `K` requests in the last `T` seconds.
**Goal:** Implement a `RateLimiter` class or function.

### Pseudocode (Queue / Deque Strategy)
```text
CLASS RateLimiter:
    dictionary 'hits' = { IP_ADDRESS : DEQUE of timestamps }
    CONSTANT LIMIT = 100
    CONSTANT WINDOW = 60 (seconds)

    FUNCTION is_allowed(ip, timestamp):
        # 1. Get the list of timestamps for this IP
        user_timestamps = hits[ip]
        
        # 2. Remove old timestamps (outside the window)
        WHILE user_timestamps IS NOT EMPTY AND 
              (timestamp - user_timestamps[0] > WINDOW):
            POP LEFT from user_timestamps
            
        # 3. Check count
        IF length(user_timestamps) < LIMIT:
            APPEND timestamp TO user_timestamps
            RETURN True (Allowed)
        ELSE:
            RETURN False (Blocked)
```

### Key Discussion Points
*   **Memory Usage:** The deque approach stores every timestamp. For millions of requests, this explodes memory.
*   **Optimization (Token Bucket):** For Principal roles, suggest "Token Bucket" or "Leaky Bucket" algorithms which only store a `count` and `last_updated` timestamp, using O(1) space.

---

## 3. Merge Overlapping Maintenance Windows
**Context:** You have a list of scheduled downtime windows `[(start, end)]`. Some overlap.
**Goal:** Return the minimum list of consolidated windows covering the same time.
**Input:** `[[1, 3], [2, 6], [8, 10], [15, 18]]`
**Output:** `[[1, 6], [8, 10], [15, 18]]`

### Pseudocode
```text
FUNCTION merge_intervals(intervals):
    IF intervals IS EMPTY: RETURN []
    
    # 1. Sort by START time. Critical step.
    SORT intervals BY start_time
    
    merged = [intervals[0]]
    
    FOR current_interval IN intervals[1:]:
        last_merged = merged[-1]
        
        # 2. Check overlap
        # If current starts BEFORE last ends
        IF current_interval.start <= last_merged.end:
            # Merge them: End is the MAX of both ends
            last_merged.end = MAX(last_merged.end, current_interval.end)
        ELSE:
            # No overlap, add as new interval
            APPEND current_interval TO merged
            
    RETURN merged
```

---

## 4. Deep JSON Diff (Configuration Drift)
**Context:** You are writing a tool to detect "Configuration Drift". You have the `expected` JSON state and the `actual` JSON state.
**Goal:** Return a list of keys that have changed or are missing. Recursive approach required.

### Pseudocode
```text
FUNCTION find_diff(obj1, obj2, current_path=""):
    diffs = []
    
    # Get all unique keys from both objects
    all_keys = SET(keys of obj1) UNION SET(keys of obj2)
    
    FOR key IN all_keys:
        path = current_path + "." + key
        
        IF key NOT IN obj1:
            ADD "Added: {path}" to diffs
        ELSE IF key NOT IN obj2:
            ADD "Removed: {path}" to diffs
        ELSE:
            val1 = obj1[key]
            val2 = obj2[key]
            
            IF val1 is DICT and val2 is DICT:
                # RECURSE
                nested_diffs = find_diff(val1, val2, path)
                ADD nested_diffs to diffs
            ELSE IF val1 != val2:
                ADD "Changed: {path} from {val1} to {val2}" to diffs
                
    RETURN diffs
```

### Python Implementation Tips
*   Use `isinstance(x, dict)` to check for recursion.
*   Handle lists: Do you match by index or content? (Interview question: "How should we handle list order?")

---

## 5. Find Top K Frequent Elements (Log Aggregation)
**Context:** You have 10GB of apache logs. Find the Top 10 most requested URLs.
**Goal:** Efficiently counting and sorting.

### Pseudocode
```text
FUNCTION top_k_urls(logs, k):
    # 1. Count frequencies
    # O(N) time
    counter = Hash Map
    FOR url IN logs:
        INCREMENT counter[url]
        
    # 2. Find Top K
    # Naive: Sort all items (O(N log N))
    # Optimized: Use Min-Heap of size K (O(N log K))
    
    heap = []
    FOR (url, count) IN counter:
        PUSH (count, url) TO heap
        IF length(heap) > k:
            POP smallest element from heap
            
    # Heap now contains the k largest elements
    SORT heap descending
    RETURN heap
```

### Discussion
*   **Python Pro Tip:** `collections.Counter(logs).most_common(k)` does exactly this in highly optimized C code. Mentioning you know the underlying Heap algo *and* the Python one-liner makes you a "Hero".
