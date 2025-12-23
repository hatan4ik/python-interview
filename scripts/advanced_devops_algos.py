"""
Advanced DevOps & Python Interview Algorithms.

This module implements key algorithms often asked in Senior/Principal DevOps interviews,
focusing on Infrastructure-as-Code logic, Log Analysis, and System Stability.

Included Algorithms:
1. resolve_build_order (Topological Sort) - For CI/CD dependency chains.
2. RateLimiter (Sliding Window) - For API protection / DDoS detection.
3. merge_maintenance_windows (Interval Merging) - For downtime scheduling.
4. deep_config_diff (Recursion) - For detecting Configuration Drift.
5. get_top_k_urls (Heap/Counter) - For efficient Log Aggregation.
"""

from collections import defaultdict, deque, Counter
import heapq
import time

# ==========================================
# 1. Dependency Resolution (Build Order)
# ==========================================
def resolve_build_order(services, dependencies):
    """
    Determines the correct build/deploy order for a set of services using Topological Sort (Kahn's Algorithm).
    
    Args:
        services (list): List of service names ['api', 'db', 'cache'].
        dependencies (list): List of tuples where (A, B) means A depends on B (B must start first).
                             Example: [('api', 'db')] -> 'db' must come before 'api'.
                             
    Returns:
        list: Services in the order they should be started.
        
    Raises:
        ValueError: If a circular dependency (cycle) is detected.
    """
    # 1. Build the Graph
    # graph: key = provider (B), value = list of dependants (A)
    # in_degree: key = service, value = count of dependencies it is waiting on
    graph = defaultdict(list)
    in_degree = {s: 0 for s in services}
    
    for dependant, provider in dependencies:
        graph[provider].append(dependant)
        in_degree[dependant] += 1
        
    # 2. Initialize Queue with services having NO dependencies (in_degree == 0)
    queue = deque([node for node in services if in_degree[node] == 0])
    build_order = []
    
    # 3. Process Queue
    while queue:
        current_service = queue.popleft()
        build_order.append(current_service)
        
        # Notify "neighbors" (services depending on current) that one dependency is resolved
        for neighbor in graph[current_service]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 4. Cycle Detection
    if len(build_order) != len(services):
        raise ValueError("Circular dependency detected! Check your architecture.")
        
    return build_order


# ==========================================
# 2. Rate Limiter (Sliding Window)
# ==========================================
class RateLimiter:
    """
    Implements a Sliding Window Rate Limiter for finding abusive IPs in logs.
    
    Concept:
    Keeps a deque of timestamps for each user.
    When a new request comes in, discard timestamps older than 'window_seconds'.
    If count of remaining timestamps < limit, allow request.
    """
    def __init__(self, limit=5, window_seconds=10):
        self.limit = limit
        self.window = window_seconds
        # Dictionary: IP -> Deque of timestamps
        self.user_requests = defaultdict(deque)
        
    def allow_request(self, user_ip, timestamp=None):
        """
        Checks if a request is allowed.
        """
        if timestamp is None:
            timestamp = time.time()
            
        history = self.user_requests[user_ip]
        
        # 1. Cleanup: Remove requests older than the window
        while history and history[0] <= timestamp - self.window:
            history.popleft()
            
        # 2. Check Limit
        if len(history) < self.limit:
            history.append(timestamp)
            return True
        else:
            return False

# ==========================================
# 3. Merge Maintenance Windows (Intervals)
# ==========================================
def merge_maintenance_windows(intervals):
    """
    Consolidates overlapping time intervals.
    
    Args:
        intervals (list of lists): [[1, 3], [2, 6], [8, 10]]
        
    Returns:
        list: Merged intervals [[1, 6], [8, 10]]
    """
    if not intervals:
        return []
        
    # CRITICAL: Sort by start time first
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # Current Start <= Last End ? -> Overlap
        if current[0] <= last_merged[1]:
            # Merge: The new end is the max of both ends
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap
            merged.append(current)
            
    return merged


# ==========================================
# 4. Deep Config Drift (JSON Diff)
# ==========================================
def find_config_drift(expected, actual, path=""):
    """
    Recursively finds differences between two dictionaries (JSON objects).
    Useful for Configuration Drift detection (Terraform vs Real State).
    
    Returns:
        list: Strings describing the differences.
    """
    diffs = []
    
    # Get all unique keys from both
    all_keys = set(expected.keys()) | set(actual.keys())
    
    for key in all_keys:
        current_path = f"{path}.{key}" if path else key
        
        if key not in expected:
            diffs.append(f"[DRIFT] Unexpected key found: '{current_path}'")
        elif key not in actual:
            diffs.append(f"[DRIFT] Missing key: '{current_path}'")
        else:
            val_exp = expected[key]
            val_act = actual[key]
            
            # Recursion for nested dicts
            if isinstance(val_exp, dict) and isinstance(val_act, dict):
                nested_diffs = find_config_drift(val_exp, val_act, current_path)
                diffs.extend(nested_diffs)
            elif val_exp != val_act:
                diffs.append(f"[DRIFT] Value mismatch at '{current_path}': Expected '{val_exp}', Found '{val_act}'")
                
    return diffs


# ==========================================
# 5. Top K Logs (Heap Strategy)
# ==========================================
def get_top_k_urls(logs, k=3):
    """
    Finds the top K most frequent URLs in a log list.
    Demonstrates knowledge of Heaps vs Sorting.
    """
    # 1. Count O(N)
    counts = Counter(logs)
    
    # 2. Heap approach O(N log K) - Better than full sort O(N log N) for huge datasets
    # heapq.nlargest does this efficiently under the hood
    return heapq.nlargest(k, counts.items(), key=lambda x: x[1])


# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    print("=== 1. Dependency Resolution ===")
    services = ['frontend', 'backend', 'db', 'redis']
    # tuple: (dependant, provider) -> 'backend' depends on 'db'
    deps = [
        ('frontend', 'backend'), 
        ('backend', 'db'), 
        ('backend', 'redis')
    ]
    print(f"Services: {services}")
    print(f"Deps: {deps}")
    try:
        order = resolve_build_order(services, deps)
        print(f"Build Order: {order} (Success)")
    except ValueError as e:
        print(e)
    print("-" * 30)

    print("=== 2. Rate Limiter ===")
    limiter = RateLimiter(limit=2, window_seconds=10)
    user = "192.168.1.5"
    t = 100
    print(f"Request 1 at t={t}:   {limiter.allow_request(user, t)}")
    print(f"Request 2 at t={t+1}: {limiter.allow_request(user, t+1)}")
    print(f"Request 3 at t={t+2}: {limiter.allow_request(user, t+2)} (Should Fail)")
    print(f"Request 4 at t={t+15}: {limiter.allow_request(user, t+15)} (New Window - Should Pass)")
    print("-" * 30)

    print("=== 3. Merge Maintenance Windows ===")
    windows = [[1, 3], [8, 10], [2, 6], [15, 18]]
    print(f"Raw: {windows}")
    print(f"Merged: {merge_maintenance_windows(windows)}")
    print("-" * 30)

    print("=== 4. Deep Config Drift ===")
    desired_state = {
        "replicas": 3,
        "image": "nginx:latest",
        "env": {"DB_HOST": "localhost", "DEBUG": "false"}
    }
    current_state = {
        "replicas": 2,  # Drift
        "image": "nginx:latest",
        "env": {"DB_HOST": "10.0.0.1", "DEBUG": "false"}, # Drift in nested
        "extra_field": "manual_change" # Drift
    }
    drifts = find_config_drift(desired_state, current_state)
    for d in drifts:
        print(d)
    print("-" * 30)
    
    print("=== 5. Top K URLs ===")
    access_logs = [
        "/home", "/login", "/home", "/dashboard", "/login", 
        "/home", "/settings", "/dashboard", "/home"
    ]
    print(f"Logs: {access_logs}")
    print(f"Top 2: {get_top_k_urls(access_logs, k=2)}")
