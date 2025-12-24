# Advanced DevOps Algorithms: The "Dirty Data" Guide
*By Aaron Maxwell (Persona)*

Welcome to the deep end. If you are reading this, you aren't just looking to pass a basic coding test. You are preparing for the "Real World" scenarios that FAANG/MANGA companies use to filter out "LeetCode Monkeys" from actual engineers.

These problems share a common theme: **The Algorithm is easy. The Data is the enemy.**

---

## 1. Credit Card Compliance (The "Clean & Sort" Trap)

**The Scenario:**  
"Here is a log file containing raw credit card dumps. Parse them, validate them, identify the issuer, and sort them by Issuer (A-Z) and then by the Card Number (High-to-Low) for a report."

**The Trap:**
1.  **Garbage In:** Inputs look like `" 4111-2222... "`, `"5555 4444..."`, or `"INVALID-CARD"`. If you write `int(card)` without cleaning, you crash.
2.  **Luhn Algorithm:** You are expected to know this or derive it quickly. It's the standard mod-10 check.
3.  **Multi-Key Sorting:** This is the killer. Sorting by one field is easy. Sorting by String (Ascending) AND Number (Descending) in one pass? That separates Seniors from Juniors.

**The Fix (Pseudocode):**
```text
FUNCTION process_batch(raw_list):
    valid_list = []
    FOR raw_string IN raw_list:
        clean_string = REMOVE_NON_DIGITS(raw_string)
        IF LUHN_CHECK(clean_string) IS VALID:
            issuer = DETECT_ISSUER(clean_string)
            last_4 = LAST_4_DIGITS(clean_string)
            APPEND {issuer, last_4, original} TO valid_list
            
    # Python Pro Tip:
    # Sort Key: (issuer, -last_4)
    # The negative sign FLIPS the sort order for numbers!
    SORT valid_list BY (issuer ASC, last_4 DESC)
    
    RETURN valid_list
```

---

## 2. Server Bin Packing (The "Knapsack" Trap)

**The Scenario:**  
"You have a single dedicated host with 64 CPU cores. You have a list of 50 microservices, each requiring a specific number of cores. Which services should we deploy to maximize CPU utilization without going over 64?"

**The Trap:**
*   This sounds like a simple loop: "Sort by smallest and add them." **WRONG.** Greedy fails here.
*   This is the **0/1 Knapsack Problem**. You either take the service (1) or you don't (0).

**The Logic:**
You need Dynamic Programming. You build a table where rows are items (services) and columns are capacities (1 to 64 cores).
*   `dp[i][w]` = Max CPU usage using a subset of the first `i` items with capacity `w`.

**The Fix (Pseudocode):**
```text
FUNCTION optimize_cpu(services, capacity):
    dp = MATRIX[services_count + 1][capacity + 1]
    
    FOR i FROM 1 TO services_count:
        cost = services[i].cost
        FOR w FROM 1 TO capacity:
            IF cost <= w:
                # Choice: Don't include OR Include (and add cost)
                dp[i][w] = MAX(dp[i-1][w], cost + dp[i-1][w-cost])
            ELSE:
                dp[i][w] = dp[i-1][w]
                
    RETURN dp[final][capacity]
```

---

## 3. Dependency Resolution (The "Graph" Trap)

**The Scenario:**  
"We have a list of infrastructure tasks. Task A depends on B. B depends on C. D depends on E. In what order should we run them? Detect if there's a loop (A->B->A)."

**The Trap:**
*   You cannot just iterate. You need a graph algorithm.
*   **Topological Sort** is the answer.

**The Logic (Kahn's Algorithm):**
1.  Calculate **In-Degree** (number of dependencies) for every node.
2.  Find nodes with `0` in-degree (no dependencies). Add them to a Queue.
3.  While Queue is not empty:
    *   Pop `node`. Add to result.
    *   For each neighbor of `node`:
        *   Decrement neighbor's in-degree.
        *   If in-degree becomes 0, push neighbor to Queue.
4.  If result length != total nodes, you have a **CYCLE**.

**The Fix (Pseudocode):**
```text
FUNCTION build_order(tasks, dependencies):
    in_degree = {task: 0}
    graph = {task: []}
    
    FOR dep, provider IN dependencies:
        graph[provider].append(dep)
        in_degree[dep]++
        
    queue = [t for t in tasks IF in_degree[t] == 0]
    order = []
    
    WHILE queue:
        current = queue.pop()
        order.append(current)
        
        FOR neighbor IN graph[current]:
            in_degree[neighbor]--
            IF in_degree[neighbor] == 0:
                queue.push(neighbor)
                
    IF len(order) < len(tasks): FAIL("Cycle Detected")
    RETURN order
```