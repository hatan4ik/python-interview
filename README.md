# 🐍 Python for DevOps Interviews: The "Engineering First" Approach

> **Mission:** To transition from "Scripting" to "Software Engineering" for infrastructure. This repository provides the exact patterns required to pass SRE/DevOps coding interviews at Verisign, FAANG, and other top-tier tech companies.

This is not just code; it is a **demonstration of competency** in reliability, automation, and systems debugging.

---

## 📋 Table of Contents

1.  [Repository Structure & Engineering Justification](#-repository-structure--engineering-justification)
2.  [Execution Instructions](#-execution-instructions)
3.  [The "Why" - Python vs. Bash](#-the-why---python-vs-bash)
4.  [Core Concepts for Interviews](#-core-concepts-for-interviews)

---

## 🏗 Repository Structure & Engineering Justification

Each script maps to a specific **competency** evaluated during the technical interview.

| Script File | Engineering Competency | Why This Matters? |
| :--- | :--- | :--- |
| **`00_python_basics.py`** | **Language Fluency** | proves you can write syntax without StackOverflow. Covers loops, functions, and types. |
| **`01_log_parsing.py`** | **Data Wrangling** | Demonstrates converting unstructured text (logs) into structured data (metrics) for analysis. |
| **`02_system_commands.py`** | **OS Interaction** | Shows how to safely interact with the kernel/shell using `subprocess` instead of dangerous `os.system`. |
| **`03_api_checks.py`** | **Network Observability** | Implements health checks (TCP/HTTP) using only the **Standard Library** (no `pip install` required). |
| **`04_data_structures.py`** | **Algorithmic Efficiency** | Proves you know when to use a `Set` (O(1)) vs a `List` (O(n)) to optimize performance. |
| **`05_algorithm_warmup.py`** | **Problem Solving** | Common whiteboard questions (recursion, string manipulation) to pass the initial coding gate. |
| **`06_bash_alternatives.sh`** | **Legacy Comparison** | A reference showing the "Old Way" vs. the Python "New Way" for explaining trade-offs. |
| **`07_concurrency.py`** | **Performance Scaling** | Demonstrates `threading` (I/O bound) vs `multiprocessing` (CPU bound) for faster automation. |
| **`08_unit_tests.py`** | **Quality Assurance** | **CRITICAL:** Shows you write tests. This is the difference between a "Scripter" and an "Engineer". |
| **`09_framework_showcase.py`**| **Ecosystem Awareness** | Highlights familiarity with industry standards like `boto3` (AWS) and `fastapi`. |
| **`10_k8s_debugging.py`** | **Platform Engineering** | **NEW:** Programmatic Kubernetes debugging. Detecting `NotReady` nodes and `CrashLoopBackOff` pods using client libraries. |
| **`11_k8s_chaos_generator.py`** | **Testing/QA** | **CHAOS ENGINEERING:** Intentionally breaks the cluster (OOM, CrashLoops, Bad PVCs) to verify your debugging tools. |
| **`12_k8s_resolution_advisor.py`** | **Automation/Remediation** | **AUTO-FIX:** Scans for issues detected by script #10 and generates the exact `kubectl` commands to fix them. |
| **`13_gitops_setup.py`** | **CI/CD / GitOps** | **DEPLOYMENT:** Installs ArgoCD and deploys a sample App (Guestbook) using GitOps principles. |

---

## 🚀 Execution Instructions

**Golden Rule:** Never run Python scripts as if they were Bash scripts.

**❌ The Wrong Way:**
```bash
./02_system_commands.py  # Relies on shebang/permissions, prone to environment issues.
```

**✅ The Professional Way:**
Explicitly invoke the interpreter. This ensures you control the runtime environment.

```bash
# General Syntax
python3 <script_name.py>

# Example: Run Kubernetes Debugging logic
python3 10_k8s_debugging.py
```

### 💥 Chaos Engineering (For Script #11)

Use this to generate "interview problems" for yourself.

1.  **Inject Failures:**
    ```bash
    python3 11_k8s_chaos_generator.py --mode all
    ```
    *Creates: CrashLoop Pods, OOM Pods, Stuck PVCs, Bad Services.*

2.  **Debug:** Now run your `10_k8s_debugging.py` to see if it catches them!

3.  **Cleanup:**
    ```bash
    python3 11_k8s_chaos_generator.py --mode clean
    ```

---

## ☸️ Kubernetes Local Setup (For Script #10)

To test `10_k8s_debugging.py` locally without a real cloud cluster:

1.  **Install Minikube:** `brew install minikube` (macOS)
2.  **Start Cluster:** `minikube start`
3.  **Troubleshoot:** If `minikube start` fails due to version/driver issues:
    ```bash
    minikube delete && minikube start
    ```
4.  **Install Lib:** `pip3 install kubernetes`

### 🛠 Kubernetes Environment Management (Cheatsheet)

When working with local clusters (especially when injecting Chaos), things break. Use these commands to manage your environment.

| Action | Command | When to use? |
| :--- | :--- | :--- |
| **Start** | `minikube start` | Resume work. |
| **Stop** | `minikube stop` | Save battery/RAM when not working. |
| **Hard Reset** | `minikube delete --all && minikube start --memory=4096 --cpus=2` | **Fixes Everything.** Use if the cluster is stuck, API is timeout, or after heavy Chaos testing. |
| **Status** | `minikube status` | Check if Control Plane is alive. |

#### 🔁 The "Pro" Workflow
The scripts in this repo are designed to work in a loop:

1.  **Bring Up:** `python3 13_gitops_setup.py` (Installs ArgoCD + Apps)
2.  **Break It:** `python3 11_k8s_chaos_generator.py --mode all` (Injects Failures)
3.  **Detect It:** `python3 10_k8s_debugging.py` (Finds the issues)
4.  **Fix It:** `python3 12_k8s_resolution_advisor.py` (Get the fix commands)

---

## 💡 The "Why" - Python vs. Bash

In an interview, you will be asked: *"Why use Python for this instead of a simple Bash script?"*

**Your Answer:**
> "Bash is great for command orchestration, but Python provides **Safety**, **Structure**, and **Testability**."

1.  **Error Handling:** Python raises exceptions and stops (Fail Fast). Bash often continues execution after a failure, leading to "cascading disasters".
2.  **Structured Data:** Bash treats everything as strings. Python has Dictionaries and Objects to model complex resources (like JSON responses from APIs).
3.  **Standard Library:** Python can handle JSON, HTTP, and threading natively. Bash requires external binaries (`jq`, `curl`) which might vary between OS versions.

---

## 🧠 Core Concepts for Interviews

Don't get caught off guard. Review these files before the call:

*   **[PYTHON_CONCEPTS.md](./PYTHON_CONCEPTS.md)**: Explains `__name__ == "__main__"`, Iterators vs. Generators, and Context Managers (`with open(...)`).
*   **[KUBERNETES_CONCEPTS.md](./KUBERNETES_CONCEPTS.md)**: **NEW:** Deep dive into Networking, Port Forwarding Myths, and Production Access Patterns.
*   **[CHEAT_SHEET_PYTHON_VS_BASH.md](./CHEAT_SHEET_PYTHON_VS_BASH.md)**: A quick translation guide to map your Bash knowledge to Python.
