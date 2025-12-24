# Senior/Principal Interview Guide: GitOps & Deployment Strategies

This document covers high-level architectural patterns and the "hard questions" asked in Senior/Principal SRE interviews regarding deployment safety, Git workflows, and GitOps.

---

## 1. Advanced Deployment Strategies

"How do you deploy code without breaking production?" is the most common design question. You must know the trade-offs of each strategy.

### 🔵 Rolling Update (The Default)
*   **Mechanism:** Replace Pods one by one (e.g., `maxUnavailable: 25%`).
*   **Pros:** Zero downtime, built into K8s Deployment object.
*   **Cons:** Hard to rollback instantly (must re-deploy old image). Traffic hits both old and new versions simultaneously during the transition (API compatibility required).
*   **Verdict:** Good for stateless apps with backward-compatible APIs.

### 🔷 Recreate Strategy
*   **Mechanism:** Kill ALL old Pods -> Start ALL new Pods.
*   **Pros:** Simple state. No version mismatch.
*   **Cons:** **DOWNTIME** occurs between kill and start.
*   **Verdict:** Use only for development or workers that process queues and can pause.

### 🟦/🟩 Blue/Green Deployment
*   **Mechanism:**
    1.  "Blue" (Current) is live.
    2.  Deploy "Green" (New) alongside Blue. Wait for it to be healthy.
    3.  Switch the Service/Ingress Load Balancer to point to Green (Atomic Switch).
*   **Pros:** Instant Rollback (switch traffic back to Blue). No mixed traffic.
*   **Cons:** Cost. Requires 2x resources (Double CPU/RAM) during deployment.
*   **Verdict:** The gold standard for critical apps where cost is secondary to reliability.
*   **Tools:** Argo Rollouts, Flagger, or manual Service patching.

### 🐤 Canary Deployment
*   **Mechanism:**
    1.  Deploy new version to a small subset (e.g., 5% of users).
    2.  Monitor metrics (Error rate, Latency).
    3.  If healthy -> Increase traffic (10% -> 50% -> 100%).
    4.  If unhealthy -> Abort and revert to 0%.
*   **Pros:** Lowest risk. Real production traffic validation.
*   **Cons:** Complex setup. Requires observability/metrics (Prometheus) and advanced ingress (Istio/Nginx).
*   **Verdict:** Essential for high-scale, high-risk distributed systems.

---

## 2. GitOps Deep Dive (The "Senior" Perspective)

**Q: "Why GitOps? Why not just `kubectl apply` from Jenkins?"**

**A: The Senior Answer focuses on Drift and Security.**
1.  **Drift Detection:** "CI/CD is 'Fire and Forget'. If I manually change a Limit in production, CI won't know. GitOps (ArgoCD) sees the drift and alerts/corrects it."
2.  **Security Perimeter:** "With CI, Jenkins needs `admin` access to the cluster. With GitOps, the cluster (ArgoCD) pulls from Git. I don't need to store Cluster Admin keys in my CI server."
3.  **Audit Trail:** "Git log is the deployment log. `git revert` is the rollback button."

**Q: "How do you handle Secrets in GitOps?"**
**A:** "Never commit raw secrets. I use:
*   **SealedSecrets (Bitnami):** Encrypts secret locally, committed to Git. Controller decrypts inside cluster.
*   **ExternalSecrets Operator:** Stores secrets in Vault/AWS Secrets Manager. The operator fetches them and creates K8s Secrets."

---

## 3. Git Questions for Staff/Principal Engineers

At this level, they won't ask "how to commit". They ask about workflows and history management.

### Q1: Merge vs. Rebase
*   **Question:** "Should we use Merge or Rebase strategies for our main branch?"
*   **Answer:**
    *   **Merge (Squash):** Best for trunk-based development. Keeps history linear (one commit per feature).
    *   **Rebase:** Cleaner local history, but **DANGEROUS** on shared branches. "Never rebase a branch others are working on (Golden Rule)."
    *   **Verdict:** "I prefer 'Squash and Merge' for Pull Requests to keep `main` clean, preserving the atomic history of features."

### Q2: Git Bisect
*   **Question:** "We introduced a regression 50 commits ago. How do you find it fast?"
*   **Answer:** "I use `git bisect`. It performs a binary search through the commit history.
    1.  `git bisect start`
    2.  `git bisect bad` (Current)
    3.  `git bisect good <commit-hash>` (Last known good)
    4.  Git checks out the middle commit. I run the test.
    5.  Repeat until the offender is found. O(log n) complexity."

### Q3: The "Reflog"
*   **Question:** "A junior engineer just hard-reset their branch and lost 3 days of work. Is it gone?"
*   **Answer:** "Likely not. I check `git reflog`. It tracks *local* HEAD movements even if they aren't part of the branch history. I can find the SHA of the lost commit and `git checkout` it."

### Q4: Cherry-Pick Risks
*   **Question:** "Why is cherry-picking considered bad practice for long-term maintenance?"
*   **Answer:** "It duplicates the commit (different SHA, same content). Later merges become confusing because Git doesn't know these changes are the same. It often leads to conflict hell. It should be used for hotfixes only, not as a workflow."

---

## 4. Implementation in this Repo

*   **Rolling Update:** Standard behavior of the Deployments in `scripts/13_gitops_setup.py`.
*   **GitOps:** Implemented via **ArgoCD** (App of Apps pattern) and **Flux CD**.
*   **Drift:** Try manually deleting a deployment deployed by ArgoCD; watch it recreate it automatically.
