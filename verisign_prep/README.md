# Verisign DevOps Python Interview Preparation Kit

**Author:** Gemini CLI Agent  
**Date:** December 21, 2025  
**Target Audience:** DevOps Engineers, SREs, Systems Engineers

---

## Preface

This repository contains a curated collection of Python scripts designed to simulate technical interview scenarios common at infrastructure-heavy companies like Verisign. The focus is strictly on **operational automation**, **system observability**, and **data processing efficiency**.

Unlike standard software engineering interviews that prioritize complex algorithms (dynamic programming, graphs), DevOps interviews prioritize **robustness**, **system interaction**, and **maintainability**.

---

## Table of Contents

1. [01. Log Parsing & Analysis](#01-log-parsing--analysis)
2. [02. System Automation & Subprocesses](#02-system-automation--subprocesses)
3. [03. API Monitoring & Reliability](#03-api-monitoring--reliability)
4. [04. Data Structures for Performance](#04-data-structures-for-performance)
5. [05. Algorithmic Warmup](#05-algorithmic-warmup)

---

## 01. Log Parsing & Analysis
**File:** `01_log_parsing.py`

### The Problem
In a production environment, you are often the first line of defense during an outage. You will be given a massive access log and asked: *"Who is attacking us?"* or *"What is the error rate?"*. You need to extract structured data from unstructured text efficiently.

### Key Concepts
*   **Regular Expressions (`re`)**: For precise pattern matching (IPs, status codes) in messy logs.
*   **`collections.Counter`**: An O(1) tool for tallying frequencies without verbose boilerplate.
*   **File Streaming**: Reading files line-by-line (`for line in f:`) to avoid MemoryError on multi-gigabyte logs.

### Engineering Insight
> **Tip:** While `string.split()` is faster, it is brittle. If the log format changes slightly (e.g., a user agent string contains a space), your code breaks. Regex is the industry standard for robustness here.

---

## 02. System Automation & Subprocesses
**File:** `02_system_commands.py`

### The Problem
Bash scripts are great, but they lack error handling and complex logic capabilities. This module demonstrates how to wrap system commands (like `df -h`) within Python to build intelligent alerts and automation logic.

### Key Concepts
*   **`subprocess.run`**: The modern, safe way to execute shell commands.
*   **Input Sanitization**: Using lists `['ls', '-l']` instead of strings to prevent Shell Injection vulnerabilities.
*   **OS Traversal**: Using `os.walk()` to recursively scan directory trees—essential for cleanup scripts (e.g., "delete all `.tmp` files older than 7 days").

### Engineering Insight
> **Warning:** Never use `os.system()`. It is deprecated, insecure, and provides no easy way to capture output. Always prefer the `subprocess` module.

---

## 03. API Monitoring & Reliability
**File:** `03_api_checks.py`

### The Problem
Services fail. Network packets get dropped. A DevOps engineer must write scripts that can verify the health of a microservice and, crucially, handle transient failures gracefully without waking up the on-call engineer for a 1-second blip.

### Key Concepts
*   **Standard Library Networking**: Using `urllib` (no third-party dependencies required), which shows deep knowledge of the language core.
*   **Exponential Backoff**: Implementing retry logic with `time.sleep()` to prevent thundering herd problems.
*   **JSON Parsing**: decoding API responses to validate deep health metrics, not just HTTP 200 OK.

### Engineering Insight
> **Best Practice:** A "healthy" HTTP 200 status code is not enough. Your check should validate the *payload* (e.g., `{"database_connected": true}`).

---

## 04. Data Structures for Performance
**File:** `04_data_structures.py`

### The Problem
Efficiency matters at scale. Comparing two lists of 100,000 servers using nested loops results in 10 billion operations (O(n²)). Using the right data structure reduces this to a fraction of a second.

### Key Concepts
*   **Set Theory**: Using `set()` for O(1) lookups and instant Intersection/Difference operations.
*   **Lambda Functions**: Writing concise, one-line functions for custom sorting logic (e.g., sorting dictionaries by a specific key).
*   **List Comprehensions**: The "Pythonic" way to transform and filter lists in a single, readable line.

---

## 05. Algorithmic Warmup
**File:** `05_algorithm_warmup.py`

### The Problem
While rare, you may still encounter basic logic puzzles. These test your ability to think about edge cases and flow control. The "Balanced Parentheses" problem is a proxy for parsing configuration files (JSON/YAML/HCL).

### Key Concepts
*   **Stacks (LIFO)**: The fundamental structure for parsing nested syntax.
*   **Modulo Operator (`%`)**: The core of cyclical logic (like FizzBuzz or Round-Robin load balancing).

### Engineering Insight
> **Note:** For the balanced brackets problem, always consider the edge case of an empty string or a string with no brackets at all.
