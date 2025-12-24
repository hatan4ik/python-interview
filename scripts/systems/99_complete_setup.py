#!/usr/bin/env python
"""
Global Environment Bootstrapper.

This script acts as the "One-Click Setup" for the entire interview environment.
It orchestrates:
1. Minikube Infrastructure (CPU/RAM checks).
2. GitOps Tooling (ArgoCD).
3. GitOps Tooling (FluxCD).

Engineering Principle: "Idempotency". You can run this script 10 times, 
and it will only do the work that is missing.
"""

import subprocess
import sys
import os

# Add src to path so we can import devops_toolkit without installing it
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(SRC_PATH)

try:
    from devops_toolkit.utils.logging import setup_logger
    from devops_toolkit.system import check_binary_exists, run_command
    from devops_toolkit.k8s.operations import start_minikube
except ImportError as e:
    print(f"Error: Could not import devops_toolkit. {e}")
    sys.exit(1)

# Configure Logging
logger = setup_logger("Bootstrap")

def run_setup_script(script_name: str):
    """Executes another Python setup script in the same directory."""
    logger.info(f"👉 triggering {script_name}...")
    try:
        # Assumes the script is in the same directory
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        
        # Pass the current PYTHONPATH or set it to include src
        env = os.environ.copy()
        current_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{SRC_PATH}:{current_pythonpath}"

        subprocess.run([sys.executable, script_path], check=True, env=env)
    except subprocess.CalledProcessError:
        logger.error(f"❌ {script_name} failed.")
        sys.exit(1)

if __name__ == "__main__":
    print("\n--- 🛠  INTERVIEW ENVIRONMENT BOOTSTRAPPER 🛠  ---\n")

    # 1. Prerequisite Checks
    for cmd in ["minikube", "kubectl", "python3"]:
        if not check_binary_exists(cmd):
            logger.error(f"❌ Critical Error: '{cmd}' is not installed.")
            sys.exit(1)

    # 2. Infrastructure Layer
    start_minikube()

    # 3. Application Layer (GitOps)
    print("\n[ Installing ArgoCD ]")
    run_setup_script("13_gitops_setup.py")

    print("\n[ Installing FluxCD ]")
    run_setup_script("14_fluxcd_setup.py")

    print("\n" + "="*60)
    print("✅✅✅  COMPLETE ENVIRONMENT READY  ✅✅✅")
    print("="*60)
    print("1. Cluster:       Running (Minikube)")
    print("2. ArgoCD:        Installed (Namespace: argocd)")
    print("3. FluxCD:        Installed (Namespace: flux-system)")
    print("\nRun 'python3 scripts/10_k8s_debugging.py' to verify health.")
    print("="*60 + "\n")
