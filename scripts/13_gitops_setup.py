#!/usr/bin/env python
import subprocess
import time
import sys
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GitOpsSetup")

def run_cmd(cmd: str, shell=False):
    """Runs a shell command and checks for errors."""
    try:
        # Split command for safety unless shell=True
        if not shell:
            cmd = cmd.split()
        subprocess.run(cmd, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}")
        logger.error(f"Error: {e.stderr.decode().strip()}")
        sys.exit(1)

def install_argocd():
    logger.info("🚀 Starting ArgoCD Installation...")

    # 1. Create Namespace
    logger.info("Creating 'argocd' namespace...")
    run_cmd("kubectl create namespace argocd", shell=True) # Shell=True to ignore error if exists

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
    
    # Write to temp file and apply
    with open("argocd_app.yaml", "w") as f:
        f.write(app_manifest)
    
    run_cmd("kubectl apply -f argocd_app.yaml")
    run_cmd("rm argocd_app.yaml", shell=True)
    logger.info("✅ Application 'guestbook' registered in ArgoCD.")

def get_admin_password():
    """Retrieves the initial admin password."""
    result = subprocess.run(
        "kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d",
        shell=True, stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip()

if __name__ == "__main__":
    print("--- GitOps (ArgoCD) Installer for Minikube ---")
    
    # Check if kubectl exists
    try:
        subprocess.run(["kubectl", "version", "--client"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        logger.error("kubectl not found. Please install it first.")
        exit(1)

    install_argocd()
    deploy_gitops_app()
    
    password = get_admin_password()
    
    print("\n🎉 \033[1mINSTALLATION COMPLETE!\033[0m")
    print("-" * 60)
    print("1. Access UI via Port Forwarding:")
    print("   $ kubectl port-forward svc/argocd-server -n argocd 8080:443")
    print(f"\n2. Login Credentials:")
    print(f"   URL:      https://localhost:8080")
    print(f"   Username: admin")
    print(f"   Password: {password}")
    print("\n3. Verify App Deployment:")
    print("   $ kubectl get pods -n guestbook")
    print("-" * 60)
