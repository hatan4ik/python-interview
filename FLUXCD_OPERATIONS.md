# Flux CD Operations Cheat Sheet

Flux CD is "Headless" by default. You operate it primarily via the **Flux CLI** or **Kubectl**.

## 1. Installing the CLI (Recommended)
While you *can* use `kubectl`, the `flux` CLI is much faster for debugging.

```bash
brew install fluxcd/tap/flux   # macOS
curl -s https://fluxcd.io/install.sh | sudo bash  # Linux
```

## 2. The "Big Two" Resources
Flux is built on **Sources** (where data comes from) and **Workloads** (what runs).

| Resource Type | Description |
| :--- | :--- |
| **GitRepository** | Defines the Git URL, branch, and polling interval. |
| **Kustomization** | Defines *which folder* in the repo to apply and *where* (target namespace). |
| **HelmRelease** | (Optional) Defines a Helm Chart to install. |

## 3. Common Operations

### 👀 Checking Status
See what is currently deployed and if it is in sync.

**Using Flux CLI:**
```bash
flux get all
flux get sources git
flux get kustomizations
```

**Using Kubectl:**
```bash
kubectl get gitrepositories -A
kubectl get kustomizations -A
```

### 🔄 Force Sync (Reconcile)
Flux polls git every X minutes (defined in `interval`). To force an update **immediately**:

**Using Flux CLI:**
```bash
# Pull latest commit from Git
flux reconcile source git podinfo

# Apply manifests from the source
flux reconcile kustomization podinfo
```

**Using Kubectl (The Hard Way):**
You must annotate the resource to trigger a reconcile.
```bash
kubectl annotate --overwrite kustomization/podinfo -n flux-system reconcile.fluxcd.io/requestedAt="$(date +%s)"
```

### ⏸ Suspend Updates (Emergency)
If a bad commit is breaking prod, stop Flux from syncing.

**Using Flux CLI:**
```bash
flux suspend kustomization podinfo
```

**Using Kubectl:**
```bash
kubectl patch kustomization podinfo -n flux-system -p '{"spec":{"suspend":true}}' --type=merge
```

**To Resume:**
```bash
flux resume kustomization podinfo
```

## 4. Debugging Issues

### "My changes aren't showing up!"

1.  **Check the Source:** Did Flux see the new commit?
    ```bash
    flux get source git podinfo
    # Look for the "Revision" hash. Does it match your git commit?
    ```

2.  **Check the Application:** Did the apply fail?
    ```bash
    flux get kustomization podinfo
    # Status should be "Ready". If "False", read the message.
    ```

3.  **Read the Logs:**
    ```bash
    # Flux has multiple controllers. Check the relevant one.
    kubectl logs -n flux-system -l app=source-controller      # Git connection issues
    kubectl logs -n flux-system -l app=kustomize-controller   # YAML validation/apply issues
    ```

## 5. Directory Structure Best Practice
Flux expects a specific repo structure (Monorepo approach is common):

```text
/apps/           # Application Manifests
  /podinfo/
    deployment.yaml
    service.yaml

/clusters/       # Flux Configuration
  /prod/
    flux-system/ # Flux components
    podinfo-kustomization.yaml  # Points to /apps/podinfo
```
