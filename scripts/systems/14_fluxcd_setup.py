#!/usr/bin/env python
import subprocess
import time
import sys
import os
from pathlib import Path

# Add src to path so we can import devops_toolkit without installing it
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(SRC_PATH)

try:
    from devops_toolkit.utils.logging import setup_logger
    from devops_toolkit.system import run_command, check_binary_exists
    from devops_toolkit.k8s.operations import wait_for_deployment
except ImportError as e:
    print(f"Error: Could not import devops_toolkit. {e}")
    sys.exit(1)

# Configure Logging
logger = setup_logger("FluxSetup")

def install_flux():
    logger.info("🚀 Starting Flux CD Installation...")

    # 1. Install Flux Manifests (The "Non-Bootstrap" way for Demos)
    # This installs the Source Controller, Kustomize Controller, Helm Controller, etc.
    logger.info("Applying Flux CD Manifests (Latest)...")
    flux_install_url = "https://github.com/fluxcd/flux2/releases/latest/download/install.yaml"
    run_command(f"kubectl apply -f {flux_install_url}", shell=True)

    # 2. Wait for Components
    logger.info("⏳ Waiting for Flux Controllers to be Ready (this may take 2-3 mins)...")
    
    components = [
        "source-controller",
        "kustomize-controller",
        "helm-controller",
        "notification-controller"
    ]

    for comp in components:
        wait_for_deployment(comp, "flux-system")
    
    logger.info("✅ Flux CD Core Services are Ready.")

def deploy_flux_app():
    """Creates a 'GitRepository' and 'Kustomization' to deploy Podinfo."""
    logger.info("📦 Deploying 'Podinfo' App via Flux CD...")
    
    # 1. Create the GitRepository source
    # This tells Flux where to pull code from.
    git_repo_manifest = """
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/stefanprodan/podinfo
  ref:
    branch: master
"""
    
    # 2. Create the Kustomization
    # This tells Flux which folder to apply.
    kustomization_manifest = """
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: podinfo
  namespace: flux-system
spec:
  interval: 10m0s
  path: ./kustomize
  prune: true
  sourceRef:
    kind: GitRepository
    name: podinfo
  targetNamespace: default
"""

    source_path = Path("flux_source.yaml")
    kustomization_path = Path("flux_kustomization.yaml")
    source_path.write_text(git_repo_manifest)
    kustomization_path.write_text(kustomization_manifest)
    try:
        run_command(f"kubectl apply -f {source_path}", shell=True)
        run_command(f"kubectl apply -f {kustomization_path}", shell=True)
    finally:
        source_path.unlink(missing_ok=True)
        kustomization_path.unlink(missing_ok=True)
    
    logger.info("✅ Flux Resources created. Monitoring 'default' namespace for Podinfo...")

def main() -> int:
    print("--- GitOps (Flux CD) Installer for Minikube ---")
    
    if not check_binary_exists("kubectl"):
        logger.error("kubectl not found. Please install it first.")
        return 1

    try:
        install_flux()
        deploy_flux_app()
    except subprocess.CalledProcessError:
        return 1
    
    print("\n🎉 \033[1mINSTALLATION COMPLETE!\033[0m")
    print("-" * 60)
    print("Flux is a 'headless' GitOps tool (no UI by default).")
    print("To verify deployment:")
    print("   1. Check Flux Status:")
    print("      $ kubectl get gitrepositories -n flux-system")
    print("      $ kubectl get kustomizations -n flux-system")
    print("\n   2. Check the App (Podinfo):")
    print("      $ kubectl get pods -n default -l app=podinfo")
    print("-" * 60)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
