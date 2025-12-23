#!/usr/bin/env python
import base64
import subprocess
import time
import logging
from pathlib import Path

logger = logging.getLogger("GitOpsSetup")

def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_cmd(cmd: str, shell: bool = False) -> subprocess.CompletedProcess:
    """Runs a shell command and checks for errors."""
    try:
        # Split command for safety unless shell=True
        if not shell:
            cmd = cmd.split()
        return subprocess.run(cmd, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}")
        logger.error(f"Error: {e.stderr.decode().strip()}")
        raise

def ensure_namespace(namespace: str) -> None:
    logger.info(f"Ensuring namespace '{namespace}' exists...")
    run_cmd(f"kubectl create namespace {namespace} --dry-run=client -o yaml | kubectl apply -f -", shell=True)

def install_argocd():
    logger.info("🚀 Starting ArgoCD Installation...")

    # 1. Create Namespace
    ensure_namespace("argocd")

    # 2. Install ArgoCD Manifests
    logger.info("Applying ArgoCD Manifests (Stable)...")
    run_cmd("kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml", shell=True)

    # 3. Wait for Components
    logger.info("⏳ Waiting for ArgoCD Server to be Ready (this may take 2-3 mins)...")
    # We wait for the repo-server first as a health indicator
    run_cmd("kubectl wait --for=condition=available deployment/argocd-repo-server -n argocd --timeout=300s", shell=True)
    run_cmd("kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=300s", shell=True)
    
    logger.info("✅ ArgoCD Core Services are Ready.")

def deploy_gitops_app():
    """Creates a declarative 'Application' CRD to deploy the Guestbook app."""
    logger.info("📦 Deploying 'Guestbook' App via GitOps...")
    
    # Define the App Manifest (The GitOps way)
    app_manifest = """
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
"""
    
    app_path = Path("argocd_app.yaml")
    app_path.write_text(app_manifest)
    try:
        run_cmd(f"kubectl apply -f {app_path}")
    finally:
        app_path.unlink(missing_ok=True)
    logger.info("✅ Application 'guestbook' registered in ArgoCD.")

def get_admin_password(retries: int = 10, delay_seconds: int = 3) -> str:
    """Retrieves the initial admin password."""
    cmd = [
        "kubectl",
        "-n",
        "argocd",
        "get",
        "secret",
        "argocd-initial-admin-secret",
        "-o",
        "jsonpath={.data.password}",
    ]
    for attempt in range(1, retries + 1):
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and result.stdout.strip():
            try:
                return base64.b64decode(result.stdout.strip()).decode().strip()
            except Exception:
                logger.error("Failed to decode admin password.")
                return ""
        if attempt < retries:
            time.sleep(delay_seconds)
    logger.warning("Admin password not available yet.")
    return ""

def main() -> int:
    configure_logging()
    print("--- GitOps (ArgoCD) Installer for Minikube ---")
    
    # Check if kubectl exists
    try:
        subprocess.run(["kubectl", "version", "--client"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        logger.error("kubectl not found. Please install it first.")
        return 1

    try:
        install_argocd()
        deploy_gitops_app()
    except subprocess.CalledProcessError:
        return 1
    
    password = get_admin_password()
    
    print("\n🎉 \033[1mINSTALLATION COMPLETE!\033[0m")
    print("-" * 60)
    print("1. Access UI via Port Forwarding:")
    print("   $ kubectl port-forward svc/argocd-server -n argocd 8080:443")
    print(f"\n2. Login Credentials:")
    print(f"   URL:      https://localhost:8080")
    print(f"   Username: admin")
    print(f"   Password: {password if password else '<pending>'}")
    print("\n3. Verify App Deployment:")
    print("   $ kubectl get pods -n guestbook")
    print("-" * 60)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
