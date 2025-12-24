# FAANG/MANGA DevOps & SRE Interview Guide

This guide bridges the gap between "I know tools" and "I understand Engineering".
Use the code in this repository to demonstrate these concepts.

## 1. System Design & Architecture

### The "GitOps" Pattern
**Question:** "How do you manage cluster state drift?"
**Answer:** "I use GitOps controllers like ArgoCD or Flux. Unlike CI pipelines (Jenkins/GitLab CI) which 'push' changes and fire-and-forget, GitOps controllers sit inside the cluster and constantly 'pull' and reconcile the state. This ensures that `git` is always the source of truth, not what an engineer manually ran via `kubectl apply`."

*   **Demo:** Show `scripts/13_gitops_setup.py`. Explain how it bootstraps the controller, which then takes over.

### Idempotency
**Question:** "What happens if I run your automation script twice?"
**Answer:** "It should succeed without side effects. My Python scripts check the state before acting (e.g., `if not check_namespace_exists(...)`). This is better than a Bash script that might fail with 'Resource already exists'."

*   **Demo:** Show `src/devops_toolkit/k8s/operations.py` -> `ensure_namespace`.

## 2. Kubernetes Deep Dive

### Debugging Workflows
**Question:** "A deployment is failing. Walk me through your debugging process."
**Answer:**
1.  **Describe:** `kubectl describe pod <pod>` to check events (ImagePullBackOff, OOMKilled).
2.  **Logs:** `kubectl logs <pod>` (check previous container with `--previous` if it crashed).
3.  **Resource:** Check CPU/Memory limits. Is the node under pressure?
4.  **Network:** Can the pod reach its dependencies? (DNS, Service endpoints).

*   **Demo:** Run `scripts/11_k8s_chaos_generator.py` to break things, then use `scripts/10_k8s_debugging.py` to programmatically find the root cause.

### Liveness vs. Readiness
**Question:** "What is the difference between Liveness and Readiness probes?"
**Answer:**
*   **Liveness:** "Am I dead?" (Restart me).
*   **Readiness:** "Am I busy?" (Don't send me traffic yet).
*   **Trap:** If a backend is down, do NOT fail the Liveness probe of the frontend, or the whole frontend layer will restart loop. Fail the Readiness probe instead.

## 3. Python for Infrastructure

### Why Python over Bash?
**Answer:** "Bash is unmanageable at scale. Python gives me:"
1.  **Testing:** I can write `unittest` or `pytest` suites (see `tests/`).
2.  **Safety:** `subprocess.run(check=True)` prevents silent failures.
3.  **Libraries:** I can use the official `kubernetes` client instead of parsing JSON text from `kubectl`.

### Concurrency
**Question:** "How would you check 1,000 servers efficiently?"
**Answer:** "I would use `ThreadPoolExecutor` for I/O bound tasks (network checks) or `multiprocessing` for CPU bound tasks (log parsing)."

*   **Demo:** `scripts/07_concurrency.py`.

## 4. The "Modularity" Story (Repo Walkthrough)

**Narrative:** "I started this project as a collection of scripts. I noticed I was copying `run_command` everywhere. I refactored it into a library (`devops_toolkit`) following standard Python packaging (`pyproject.toml`). This allows me to version the tooling and install it anywhere."

**Key Files to Show:**
1.  `pyproject.toml` (The "Engineering" standard).
2.  `src/devops_toolkit/system.py` (The shared logic).
3.  `tests/` (The quality assurance).

## 5. Git Mastery & Deployment Strategies

**Question:** "How do you handle Git in production and during incidents?"
**Answer:** "I optimize for safety and rollback. I do not rewrite shared history; I use `revert` on main, `reflog` for recovery, and `bisect` to pinpoint regressions. In GitOps, I roll back by reverting Git so the cluster converges back to the desired state."

*   **Deep Dive:** See **[ADVANCED_DEPLOYMENT_STRATEGIES.md](./ADVANCED_DEPLOYMENT_STRATEGIES.md)** for senior-level Q/A (Blue/Green, Canary) and Git recovery playbooks.

## 6. Mock Interview Questions (To Ask Yourself)

1.  *Design a system to rotate logs on 10k servers.*
2.  *What happens when you type `google.com` in your browser? (DNS -> TCP -> TLS -> HTTP).*
3.  *How do you handle secrets in Kubernetes? (SealedSecrets, Vault, ExternalSecrets).*

## 7. Coding Round Drills (FAANG Core Patterns)

1.  *Two Sum* -> Hash Map, O(N). (See `scripts/interview_practice_set.py`)
2.  *Valid Parentheses* -> Stack.
3.  *Longest Substring Without Repeating Characters* -> Sliding Window.
4.  *Minimum Window Substring* -> Sliding Window + Frequency Map.
5.  *Product of Array Except Self* -> Prefix/Suffix.
6.  *Merge Intervals* -> Sort + Merge.
7.  *Binary Search* -> Standard and Rotated Array variants.
8.  *Subarray Sum Equals K* -> Prefix Sum + Hash Map.
9.  *Number of Islands* -> DFS/BFS on grid.
10. *Kth Largest Element* -> Quickselect or Heap.

## 8. Systems Coding Exercises (SRE Flavor)

1.  *Build Order from Dependencies* (Topological Sort).
2.  *Rate Limiter* (Sliding Window vs Token Bucket).
3.  *Config Drift Detector* (Deep JSON Diff).
4.  *Top K URLs from Logs* (Counter + Min-Heap).
5.  *Merge Maintenance Windows* (Intervals).
