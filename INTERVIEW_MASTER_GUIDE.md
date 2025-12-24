# 🧠 The Master Guide: Python & DevOps Interview Logic

> **Objective:** This index ties together the "Meta-Skill" of interviewing with the specific Algorithms and System Design patterns required for Senior/Principal DevOps roles.

**How to use this guide:**
Follow the phases in order. Do not skip Phase 1.

---

## 🗺️ Phase 1: The Methodology (The "Meta-Game")
*Before writing code, you must master the process.*

*   **File:** [`PSEUDOCODE_METHODOLOGY.md`](./PSEUDOCODE_METHODOLOGY.md)
*   **What you will learn:**
    1.  **The "3-Pass Read":** How to scan a problem for constraints without panicking.
    2.  **Structuring Pseudocode:** How to write logic that looks professional (not just "Python on paper").
    3.  **The "Talk-Write" Protocol:** How to narrate your thoughts to get partial credit even if you fail the syntax.

---

## 💻 Phase 2: The Coding Round (Strings & Lists)
*The "Gatekeeper" questions. You must solve these quickly and cleanly.*

*   **File:** [`INTERVIEW_PSEUDOCODE_GUIDE.md`](./INTERVIEW_PSEUDOCODE_GUIDE.md)
*   **Key Algorithms:**
    *   **Sentence Reconstruction:** Index-based sorting.
    *   **Credit Card Validation:** Luhn Algorithm + Multi-key Sorting.
    *   **Log Reordering:** Custom Sort Keys (Stability).
    *   **Version Compare:** String parsing & padding.
    *   **Group Anagrams:** HashMap (Dictionary) grouping strategy.

---

## 🏗️ Phase 3: The System Design Round (Infra Logic)
*Senior/Principal level questions. "Design a Rate Limiter" or "Resolve Dependencies".*

*   **File:** [`ADVANCED_DEVOPS_ALGO_GUIDE.md`](./ADVANCED_DEVOPS_ALGO_GUIDE.md)
*   **Key Algorithms:**
    *   **Build Order:** Topological Sort (Kahn's Algo).
    *   **Rate Limiter:** Sliding Window (Deque) vs. Token Bucket.
    *   **Maintenance Windows:** Interval Merging.
    *   **Config Drift:** Recursive DFS (Deep Diff).
    *   **Log Aggregation:** Min-Heaps for Top-K items.

---

## ⚡ Phase 4: The "Cheat Sheet" (Quick Recall)

### ⏱️ Time Complexity Rules of Thumb

| Scenario | Complexity | Good/Bad? |
| :--- | :--- | :--- |
| **Hash Map / Set Lookup** | $O(1)$ | **Excellent** (Instant) |
| **Binary Search** (Sorted Data) | $O(\log N)$ | **Great** (Scales huge) |
| **One Loop** (Linear Scan) | $O(N)$ | **Good** (Standard) |
| **Sorting** (Merge/Quick/Tim) | $O(N \log N)$ | **Acceptable** (Limit for large data) |
| **Nested Loops** (Bubble Sort) | $O(N^2)$ | **FAIL** (Timeout on big inputs) |

### 🛠️ Data Structure Selection Guide

| If the problem involves... | Use this Python Tool... | Why? |
| :--- | :--- | :--- |
| **Unique items** / Fast lookup | `set()` | O(1) check vs O(N) list scan. |
| **Counting items** | `collections.Counter` | Optimized C-based counting. |
| **First-In-First-Out (Queue)** | `collections.deque` | `pop(0)` on list is O(N). Deque is O(1). |
| **Top K items** / Priority | `heapq` | Faster than sorting the whole list. |
| **Grouping data** | `defaultdict(list)` | No need to check `if key in dict`. |

### 🧩 Pattern Recognition

*   **"Find the shortest path..."** $\rightarrow$ **BFS** (Breadth-First Search).
*   **"Find all combinations..."** $\rightarrow$ **DFS** (Recursion/Backtracking).
*   **"Sorted Array..."** $\rightarrow$ **Binary Search** or **Two Pointers**.
*   **"Top K elements..."** $\rightarrow$ **Heap** (Priority Queue).
*   **"Common elements..."** $\rightarrow$ **Set Intersection**.
*   **"Palindrome / Substring"** $\rightarrow$ **Two Pointers** (Start/End) or **Sliding Window**.

---

## 🗓️ The Daily Drill (Study Schedule)

*   **Day 1:** Read [`PSEUDOCODE_METHODOLOGY.md`](./PSEUDOCODE_METHODOLOGY.md). Practice writing *only* pseudocode for "Move Zeroes".
*   **Day 2:** Master `INTERVIEW_PSEUDOCODE_GUIDE.md`. Implement "Credit Card Processing" from scratch.
*   **Day 3:** Dive into `ADVANCED_DEVOPS_ALGO_GUIDE.md`. Understand "Topological Sort" (Build Order).
*   **Day 4:** Run `scripts/advanced_devops_algos.py` and modify the inputs to break the code.
*   **Day 5:** Mock Interview. Pick a random problem from Phase 2/3 and use the "Talk-Write" protocol.
