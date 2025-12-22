# Verisign DevOps Python Interview Prep

**Goal**: Master the core Python patterns required for infrastructure and reliability engineering interviews (SRE/DevOps).

This repository contains 5 targeted scripts designed to cover the 80/20 of technical interview questions: Log parsing, System interaction, API monitoring, Data structures, and Basic algorithms.

## Table of Contents
- [01. Log Parsing & Regex](#01-log-parsing--regex)
- [02. System Commands & Automation](#02-system-commands--automation)
- [03. API Health Checks](#03-api-health-checks)
- [04. Data Structures & Efficiency](#04-data-structures--efficiency)
- [05. Algorithms Warmup](#05-algorithms-warmup)
- [Execution Instructions](#execution-instructions)

---

### 01. Log Parsing & Regex
**File**: `01_log_parsing.py`

**Objective**:
Parse a raw web server log file to extract traffic metrics, specifically counting HTTP 500 errors and identifying high-traffic IP addresses. This mimics real-world incident investigation.

**Engineering Concepts**:
- **Regular Expressions (`re`)**: Robust pattern matching for unstructured text.
- **`collections.Counter`**: High-performance dictionary subclass for counting hashable objects.
- **File I/O Context Managers**: Using `with open(...)` to ensure file handle safety.

**Roiely's Insight**:
> "In an interview, always offer two solutions: 'I can split the string by spaces for speed, or use Regex for robustness.' It shows you understand trade-offs. Also, `Counter` is your best friend for 'top N' questions."

---

### 02. System Commands & Automation
**File**: `02_system_commands.py`

**Objective**:
Interact with the underlying OS to monitor resources (Disk Usage) and traverse file systems. This replaces fragile Bash scripts with structured Python.

**Engineering Concepts**:
- **`subprocess.run`**: The modern standard for invoking shell commands (replacing `os.system`).
- **`shlex.split`**: Security best practice to prevent shell injection attacks.
- **`os.walk`**: Recursive directory traversal generator used for finding files.

**Roiely's Insight**:
> "Never parse command output blindly. Always check exit codes (`check=True`) and handle exceptions. A script that fails silently is worse than no script at all. Security (shlex) is a huge plus."

---

### 03. API Health Checks
**File**: `03_api_checks.py`

**Objective**:
Implement a synthetic monitoring check for a microservice using standard libraries. Includes logic for retries to handle transient network failures.

**Engineering Concepts**:
- **Standard Lib (`urllib`)**: Using built-ins to avoid external dependencies (crucial in restricted environments).
- **JSON Parsing**: Converting API responses to native Python dictionaries.
- **Retry Logic**: Implementing exponential backoff (or simple delays) for resilience.

**Roiely's Insight**:
> "Using `requests` is easy. Using `urllib` proves you know the language deeply. If you use `urllib`, tell the interviewer: 'In production, I'd use `requests` for readability, but here's how to do it with standard tools.' That awareness is key."

---

### 04. Data Structures & Efficiency
**File**: `04_data_structures.py`

**Objective**:
Demonstrate mastery of Python's core data structures (Lists, Sets, Dicts) to solve common data manipulation tasks efficiently (O(n) vs O(n^2)).

**Engineering Concepts**:
- **Set Theory**: Using `intersection` for rapid comparison of large datasets.
- **Lambda Functions**: Inline functions for custom sorting keys.
- **List/Set Comprehensions**: Pythonic, concise syntax for filtering and transformation.

**Roiely's Insight**:
> "Complexity matters. Transforming a List to a Set for membership checks changes an operation from O(n) to O(1). Mentioning Big-O notation when choosing your data structure is a quick way to look like a senior engineer."

---

### 05. Algorithms Warmup
**File**: `05_algorithm_warmup.py`

**Objective**:
Solve classic logic puzzles that test basic problem-solving skills without requiring advanced CS theory.

**Engineering Concepts**:
- **Stacks (LIFO)**: Using lists as stacks to validate nested structures (Balanced Brackets).
- **Modulo Arithmetic**: Core logic for periodic conditions (FizzBuzz variants).

**Roiely's Insight**:
> "Don't just write code; talk through your edge cases. 'What if the string is empty?' 'What if the input is non-numeric?' Communication is 50% of the grade. Also, Balanced Brackets is a very common infrastructure-as-code validation question."

---

### Execution Instructions

To run any script, simply execute it with python:

```bash
python 01_log_parsing.py
```

*Note: `01_log_parsing.py` will generate a `server.log` file in the current directory as part of its execution.*