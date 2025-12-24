# 🧠 The "Aaron Maxwell" Pseudocode Library
**Consolidated Logic Patterns for DevOps Interviews**

This document strips away the syntax and focuses purely on the *Logic*. If you can write the pseudocode, the Python is easy.

---

## 1. Multi-Key Sorting (The "Credit Card" Problem)

**The Challenge:** Sort a list of items by 3 different criteria.
1.  **Priority Enum** (e.g., specific brand order: Amex > Visa).
2.  **Date** (Ascending).
3.  **Number** (Descending).

**The "Pro" Logic:**
Don't write three sort loops. Use a **Tuple Key**.

```text
FUNCTION sort_complex_items(items):
    DEFINE mapping_table = {"Amex": 1, "Visa": 2, "Mastercard": 3}

    FUNCTION get_sort_key(item):
        priority = mapping_table[item.type]
        date_val = PARSE_DATE(item.date)
        # TRICK: To sort descending in an ascending sort, NEGATE the number.
        num_val  = -INT(item.last_four) 
        
        RETURN (priority, date_val, num_val)

    # Python's Timsort uses this tuple to compare element by element.
    # If priorities match, it checks date. If dates match, it checks number.
    SORT items USING get_sort_key
    RETURN items
```

---

## 2. Rate Limiter (The "Log Window" Problem)

**The Challenge:** Only allow 1 log per user every `N` seconds.

**The "Pro" Logic:**
Use a **Hash Map** to track state.

```text
FUNCTION rate_limit(stream, window):
    DEFINE last_seen_map = {}  # Key: UserID, Value: Timestamp
    DEFINE output = []

    FOR EACH (timestamp, user, msg) IN stream:
        IF user NOT IN last_seen_map:
            APPEND log TO output
            last_seen_map[user] = timestamp
        ELSE:
            previous_time = last_seen_map[user]
            IF (timestamp - previous_time) > window:
                APPEND log TO output
                last_seen_map[user] = timestamp  # Update to NEW time
            ELSE:
                DISCARD log (Too soon)
    
    RETURN output
```

---

## 3. Sentence Reconstruction (Index:Word)

**The Challenge:** Given `["9:dog", "1:The"]`, build the sentence.

**The "Pro" Logic:**
Parse -> Sort -> Extract.

```text
FUNCTION reconstruct(list_a, list_b):
    COMBINE list_a + list_b INTO raw_list
    DEFINE parsed_list = []

    FOR item IN raw_list:
        SPLIT item BY ":" INTO (index_str, word_str)
        # SANITIZE!
        index = STRING_TO_INT(index_str.TRIP())
        word  = word_str.STRIP()
        APPEND (index, word) TO parsed_list

    # Sort based on the first element (Index)
    SORT parsed_list BY index

    # Extract just the words
    final_words = [word FOR (index, word) IN parsed_list]
    
    RETURN JOIN(final_words, " ") + "."
```

---

## 4. Dependency Resolution (The "Boot Order" Problem)

**The Challenge:** Service A needs B. B needs C. Start in order: C -> B -> A.

**The "Pro" Logic:**
**Topological Sort (Kahn's Algorithm)**.

```text
FUNCTION resolve_dependencies(service_map):
    # 1. Calculate "In-Degree" (How many things does this node need?)
    DEFINE in_degree = {all_nodes: 0}
    DEFINE graph = {}

    FOR service, dependencies IN service_map:
        FOR dep IN dependencies:
            graph[dep].APPEND(service) # Dep points TO Service
            in_degree[service] += 1

    # 2. Find starters (Nodes with 0 dependencies)
    queue = [nodes WHERE in_degree == 0]
    result = []

    # 3. Process
    WHILE queue IS NOT EMPTY:
        current = queue.POP()
        APPEND current TO result

        FOR neighbor IN graph[current]:
            in_degree[neighbor] -= 1
            IF in_degree[neighbor] == 0:
                queue.APPEND(neighbor)

    RETURN result
```
