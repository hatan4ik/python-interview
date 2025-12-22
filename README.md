# 🚀 Python & Bash DevOps Interview Prep

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Bash](https://img.shields.io/badge/Bash-4.0%2B-green?style=for-the-badge&logo=gnu-bash)
![Status](https://img.shields.io/badge/Status-Interview--Ready-success?style=for-the-badge)

**Goal**: A comprehensive "Zero to Hero" study guide for SRE/DevOps technical interviews. 
This repository covers the spectrum from **Log Parsing** and **System Automation** to **Concurrency** and **Unit Testing**, providing both the code and the "why" behind it.

## 📚 Table of Contents
- [01. Log Parsing & Regex](#01-log-parsing--regex)
- [02. System Commands (Pathlib & Subprocess)](#02-system-commands--automation)
- [03. API Health Checks (Resilience)](#03-api-health-checks)
- [04. Data Structures (Big-O Optimization)](#04-data-structures--efficiency)
- [05. Algorithmic Thinking](#05-algorithms-warmup)
- [06. Bash Alternatives (The "Right Tool" Check)](#06-bash-alternatives)
- [07. Concurrency & Scaling (Advanced)](#07-concurrency--scaling)
- [08. Unit Testing & QA (Advanced)](#08-unit-testing--qa)
- [Cheat Sheet: Python vs Bash](CHEAT_SHEET_PYTHON_VS_BASH.md)
- [References & Further Reading](#-references--links-to-work)

---

### 01. Log Parsing & Regex
**File**: [`01_log_parsing.py`](./01_log_parsing.py)

**The Task**: Parse a raw access log to count 500 errors and find the top traffic sources.
**Key Concepts**: `re` (Regex), `collections.Counter`, `pathlib`.
**Why it matters**: This is the #1 DevOps interview question. It tests your ability to turn unstructured text into structured metrics.

### 02. System Commands & Automation
**File**: [`02_system_commands.py`](./02_system_commands.py)

**The Task**: Monitor disk usage and traverse directory trees to find large files.
**Key Concepts**: `subprocess.run` (Safe Shelling), `shlex.split`, `Path.rglob` (Recursive Search).
**Why it matters**: Replaces fragile shell scripts with robust, cross-platform Python.

### 03. API Health Checks
**File**: [`03_api_checks.py`](./03_api_checks.py)

**The Task**: Monitor a microservice's JSON endpoint with retry logic for network resilience.
**Key Concepts**: `urllib` (Standard Lib), `http.HTTPStatus`, `json` parsing, `time.sleep` (Backoff).
**Why it matters**: Demonstrates how you handle distributed systems and transient failures.

### 04. Data Structures & Efficiency
**File**: [`04_data_structures.py`](./04_data_structures.py)

**The Task**: Efficiently sort users and find common servers between clusters.
**Key Concepts**: `Set` Intersection (O(1) vs O(N)), `TypedDict`, Lambda sorting keys.
**Why it matters**: Shows you care about performance and complexity, not just "getting it to work."

### 05. Algorithms Warmup
**File**: [`05_algorithm_warmup.py`](./05_algorithm_warmup.py)

**The Task**: Validate configuration syntax (Balanced Brackets) and logic loops (FizzBuzz).
**Key Concepts**: Stack (LIFO) data structures, Modulo arithmetic.
**Why it matters**: Validating JSON/YAML/HCL config files is a daily task for SREs.

### 06. Bash Alternatives
**File**: [`06_bash_alternatives.sh`](./06_bash_alternatives.sh)

**The Task**: Solve the exact same problems using `awk`, `sed`, `grep`, and `curl`.
**Key Concepts**: Unix Pipes, Text Stream Processing.
**Why it matters**: Knowing *when* to use Bash vs Python is the mark of a Senior Engineer.
> **See the Guide**: [Python vs Bash Cheat Sheet](./CHEAT_SHEET_PYTHON_VS_BASH.md)

### 07. Concurrency & Scaling
**File**: [`07_concurrency.py`](./07_concurrency.py)

**The Task**: Check health status of multiple servers in parallel.
**Key Concepts**: `concurrent.futures.ThreadPoolExecutor`, I/O Bound vs CPU Bound.
**Why it matters**: "How does this script scale to 10,000 servers?" This is the answer.

### 08. Unit Testing & QA
**File**: [`08_unit_tests.py`](./08_unit_tests.py)

**The Task**: Verify the correctness of the algorithms without running them manually.
**Key Concepts**: `unittest` framework, Edge case coverage.
**Why it matters**: Code without tests is technical debt. This proves you write production-grade software.

---

## 🔗 References & Links to Work

### Official Documentation (The Source of Truth)
*   **Pathlib**: [Python 3 `pathlib` Documentation](https://docs.python.org/3/library/pathlib.html) - Object-oriented filesystems.
*   **Threading**: [Python `concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) - Launching parallel tasks.
*   **Subprocess**: [Python `subprocess` Module](https://docs.python.org/3/library/subprocess.html) - Spawning new processes.
*   **Typing**: [Python Type Hints (`typing`)](https://docs.python.org/3/library/typing.html) - Writing modern, safe code.

### Industry Standard Reading
*   **Google SRE Book**: [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) - The "Bible" of our field.
*   **The Twelve-Factor App**: [12factor.net](https://12factor.net/) - Modern application methodology.

---

## 🛠 Execution

**Run Python Scripts:**
```bash
./01_log_parsing.py
# OR
python3 01_log_parsing.py
```

**Run Bash Scripts:**
```bash
./06_bash_alternatives.sh
```

**Run Tests:**
```bash
./08_unit_tests.py
```
