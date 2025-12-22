# 🚀 Python & Bash DevOps Interview Prep

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Bash](https://img.shields.io/badge/Bash-4.0%2B-green?style=for-the-badge&logo=gnu-bash)
![Status](https://img.shields.io/badge/Status-Interview--Ready-success?style=for-the-badge)

**Goal**: A comprehensive "Zero to Hero" study guide for SRE/DevOps technical interviews. 
This repository covers the spectrum from **Log Parsing** and **System Automation** to **Concurrency** and **Unit Testing**, providing both the code and the "why" behind it.

## 📚 Table of Contents
- [00. Python Basics (Start Here)](#00-python-basics-start-here)
- [01. Log Parsing & Regex](#01-log-parsing--regex)
- [02. System Commands (Pathlib & Subprocess)](#02-system-commands--automation)
- [03. API Health Checks (Resilience)](#03-api-health-checks)
- [04. Data Structures (Big-O Optimization)](#04-data-structures--efficiency)
- [05. Algorithmic Thinking](#05-algorithms-warmup)
- [06. Bash Alternatives (The "Right Tool" Check)](#06-bash-alternatives)
- [07. Concurrency & Scaling (Advanced)](#07-concurrency--scaling)
- [08. Unit Testing & QA (Advanced)](#08-unit-testing--qa)
- [09. Framework Showcase (Requests, Boto3, FastAPI)](#09-framework-showcase)
- [Cheat Sheet: Python vs Bash](CHEAT_SHEET_PYTHON_VS_BASH.md)
- [Concepts: The "No Surprises" Guide](PYTHON_CONCEPTS.md)

---

### 09. Framework Showcase
**File**: [`09_framework_showcase.py`](./09_framework_showcase.py)

**The Task**: Code examples for the "Big Three" DevOps frameworks: **Requests** (HTTP), **Boto3** (AWS), and **FastAPI**.
**Key Concepts**: External Libraries, Mocking (simulating cloud/web calls).
**Why it matters**: These are the specific tools 90% of DevOps jobs require. Knowing the syntax by heart is a superpower.

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
