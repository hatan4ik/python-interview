# 🐍 Python for DevOps Interviews: The "No Fluff" Guide

> **Objective:** A curated collection of Python scripts designed to bridge the gap between "Bash scripting" and "Software Engineering" for DevOps roles at top-tier tech companies (FAANG/MANGA).

This repository is structured to demonstrate **production-readiness**, **testability**, and **systems thinking**—traits highly valued in modern SRE/DevOps interviews.

---

## 📋 Table of Contents

1.  [How to Run the Scripts](#-how-to-run-the-scripts) (Critical!)
2.  [Repository Structure & Engineering Context](#-repository-structure--engineering-context)
3.  [Why Python over Bash?](#-why-python-over-bash)
4.  [Core Concepts & Interview Cheat Sheet](#-core-concepts--interview-cheat-sheet)

---

## 🚀 How to Run the Scripts

**Common Mistake:** Running Python files as Shell scripts.
*   ❌ `sh ./02_system_commands.py` -> **FAIL** (Syntax Error)
*   ❌ `./02_system_commands.py` -> **RISKY** (Depends on system `python` path/permissions)

**✅ The Correct Way:**
Explicitly invoke the python interpreter.

```bash
# General Usage
python3 <script_name.py>

# Example: Run the System Commands script
python3 02_system_commands.py

# Example: Run the Unit Tests
python3 08_unit_tests.py
```

---

## 🏗 Repository Structure & Engineering Context

Each script targets a specific competency area evaluated in interviews.

| File | Engineering Goal (The "Why") | Key Concepts |
| :--- | :--- | :--- |
| **`00_python_basics.py`** | **Syntax Fluency.** Proving you know the language fundamentals without Googling. | Variables, Loops, Functions, Types. |
| **`01_log_parsing.py`** | **Data Processing.** Converting unstructured logs into actionable metrics (Structured Data). | File I/O, String Manipulation, Regex, Dicts. |
| **`02_system_commands.py`** | **Automation Safety.** Replacing fragile `sed/awk` chains with robust, readable automation. | `subprocess`, `pathlib`, Error Handling. |
| **`03_api_checks.py`** | **Observability.** Monitoring service health via HTTP/TCP checks. | `socket`, `urllib` (Standard Lib only). |
| **`04_data_structures.py`** | **Optimization.** Using the right tool for the job to reduce Time Complexity. | `Set` (O(1) lookup), `Dict`, `List`. |
| **`05_algorithm_warmup.py`** | **Problem Solving.** Passing the "Phone Screen" coding gates. | Stack, Queues, Recursion. |
| **`06_bash_alternatives.sh`** | **Context.** A reference to show *how* the Python scripts improve upon legacy Bash. | Comparison. |
| **`07_concurrency.py`** | **Performance.** Executing tasks in parallel (I/O bound vs CPU bound). | `threading` vs `multiprocessing`. |
| **`08_unit_tests.py`** | **Reliability.** Ensuring code changes don't cause regressions (Bugs). | `unittest`, Test Driven Development (TDD). |
| **`09_framework_showcase.py`**| **Ecosystem.** Demonstrating familiarity with standard DevOps libraries. | `boto3` (AWS), `fastapi`, `requests`. |

---

## 💡 Why Python over Bash?

While Bash is excellent for "glue code" and simple one-liners, it becomes a liability in complex systems.

1.  **Error Handling:** Bash continues running after errors by default; Python raises Exceptions that stop execution immediately (Safety).
2.  **Data Structures:** Bash lacks true arrays/dictionaries/objects. Python's `dict` and `class` allow modeling complex infrastructure state.
3.  **Testability:** You cannot effectively unit test Bash scripts. Python allows for TDD (Test Driven Development).
4.  **Readability:** Python code is often self-documenting. Complex Bash scripts (`awk '{print $2}' | sed ...`) become "Write Only" code.

*See `CHEAT_SHEET_PYTHON_VS_BASH.md` for a syntax comparison.*

---

## 🧠 Core Concepts & Interview Cheat Sheet

We have prepared deep-dive documentation to handle theoretical questions:

*   **[PYTHON_CONCEPTS.md](./PYTHON_CONCEPTS.md)**: Explanations of `__name__ == "__main__"`, Iterators, Generators, Decorators, and more.
*   **[CHEAT_SHEET_PYTHON_VS_BASH.md](./CHEAT_SHEET_PYTHON_VS_BASH.md)**: Quick syntax translation guide.