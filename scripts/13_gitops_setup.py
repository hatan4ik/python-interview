#!/usr/bin/env python
import subprocess
import time
import sys
import os
import base64
from pathlib import Path

# Add src to path so we can import devops_toolkit without installing it
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(SRC_PATH)

try:
    from devops_toolkit.utils.logging import setup_logger
    from devops_toolkit.system import run_command, check_binary_exists
    from devops_toolkit.k8s.operations import ensure_namespace, wait_for_deployment
except ImportError as e:
    print(f"Error: Could not import devops_toolkit. {e}")
    sys.exit(1)

# Configure Logging
logger = setup_logger("GitOpsSetup")

def install_argocd():
    logger.info("🚀 Starting ArgoCD Installation...")

    # 1. Create Namespace
    ensure_namespace("argocd")

    # 2. Install ArgoCD Manifests
    logger.info("Applying ArgoCD Manifests (Stable)...")
    run_command("kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml", shell=True)

    # 3. Wait for Components
    logger.info("⏳ Waiting for ArgoCD Server to be Ready (this may take 2-3 mins)...")
    # We wait for the repo-server first as a health indicator
    wait_for_deployment("argocd-repo-server", "argocd")
    wait_for_deployment("argocd-server", "argocd")
    
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
        run_command(f"kubectl apply -f {app_path}", shell=True)
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
        try:
            result = run_command(cmd, capture_output=True)
            if result.stdout.strip():
                try:
                    return base64.b64decode(result.stdout.strip()).decode().strip()
                except Exception:
                    logger.error("Failed to decode admin password.")
                    return ""
        except subprocess.CalledProcessError:
            pass
        
        if attempt < retries:
            time.sleep(delay_seconds)
    logger.warning("Admin password not available yet.")
    return ""

def main() -> int:
    print("--- GitOps (ArgoCD) Installer for Minikube ---")
    
    if not check_binary_exists("kubectl"):
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
