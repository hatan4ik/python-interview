# From Single Script to Modular Architecture

## The Evolution of a Codebase

In the beginning, there were scripts. Single files, easy to write, easy to run. But as the project grew, so did the pain.
Copy-pasting `run_cmd` functions, inconsistent logging, and the fear of breaking one script while fixing another became the norm.

To meet "FAANG/MANGA" engineering standards, we evolved.

## The "DevOps Toolkit" Pattern

We refactored the codebase into a robust, installable Python package: `devops_toolkit`.

### 1. Structure
We moved from a flat structure to a `src` layout:

```text
/
├── src/
│   └── devops_toolkit/
│       ├── __init__.py
│       ├── system.py       <-- Unified command execution
│       ├── utils/
│       │   └── logging.py  <-- Standardized logging
│       └── k8s/
│           ├── client.py
│           └── operations.py <-- Idempotent K8s actions
├── scripts/
│   ├── 99_complete_setup.py  <-- Thin wrapper / Orchestrator
│   └── ...
├── pyproject.toml            <-- Modern packaging config
└── ...
```

### 2. Key Improvements

*   **DRY (Don't Repeat Yourself):** The `run_command` logic, previously duplicated 4+ times, now lives in `src/devops_toolkit/system.py`.
*   **Idempotency:** Operations like `start_minikube` and `ensure_namespace` check the current state before acting, making the scripts safe to run repeatedly.
*   **Packaging:** With `pyproject.toml`, the toolkit is a first-class citizen. It can be installed (`pip install -e .`) or distributed.
*   **Path Management:** Scripts in `scripts/` utilize `sys.path` injection (or proper installation) to robustly find their dependencies, ensuring they work out-of-the-box.

### 3. Verification Strategy (Tests)

Modularity allows for testability. We added a `tests/` directory to verify our core logic without needing a running cluster.

*   **Unit Tests:** `tests/test_system.py` mocks `subprocess.run` to ensure our command wrapper handles errors correctly.
*   **Safety:** We can now modify the core library with confidence, knowing that `python -m unittest discover tests` will catch regressions.

## How to Use

### Setup

For the best development experience, install the package in editable mode:

```bash
pip install -e .
```

### Running Scripts

The scripts in `scripts/` are now "consumers" of the toolkit.

```bash
python3 scripts/99_complete_setup.py
```

This command acts as the master orchestrator, leveraging `devops_toolkit` to safely and reliably provision the entire environment.